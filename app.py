import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from database import SessionLocal
from models import Patient, MaternalRecord

st.set_page_config(page_title="Klasifikasi Risiko Kesehatan Maternal", layout="wide")

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

def _predict_sample(node, x):
    if node.value is not None:
        return node.value
    if x[node.feature] <= node.threshold:
        return _predict_sample(node.left, x)
    return _predict_sample(node.right, x)

def _predict(tree, X):
    return np.array([_predict_sample(tree, x) for x in X])

class ScratchDecisionTree(BaseEstimator, ClassifierMixin):
    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.tree_ = None

    def fit(self, X, y):
        raise NotImplementedError("Training is done in the notebook; this stub supports unpickling and predict.")

    def predict(self, X):
        X = np.array(X)
        return _predict(self.tree_, X)

@st.cache_resource
def load_models():
    dt_bundle_paths = [
        "model/maternal_health_dt_model_fix.pkl",
        "maternal_health_dt_bundle.pkl" 
    ]

    dt_data = None
    for path in dt_bundle_paths:
        try:
            dt_data = joblib.load(path)
            break
        except FileNotFoundError:
            continue

    if dt_data is None:
        raise FileNotFoundError(
            "Decision Tree bundle not found. Expected one of: " + ", ".join(dt_bundle_paths)
        )

    rf_data = joblib.load('model/maternal_health_rf_model.pkl')
    return dt_data, rf_data

def create_patient(name, email, phone_number, address):
    db = SessionLocal()
    try:
        new_patient = Patient(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address
        )
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return True, "Data Pasien berhasil ditambahkan", new_patient.id
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}", None
    finally:
        db.close()

def update_patient(patient_id, name, email, phone_number, address):
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.name = name
            patient.email = email
            patient.phone_number = phone_number
            patient.address = address
            db.commit()
            return True, "Data Pasien berhasil diubah"
        return False, "Pasien tidak ditemukan"
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}"
    finally:
        db.close()

def delete_patient(patient_id):
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            db.query(MaternalRecord).filter(MaternalRecord.patient_id == patient_id).delete()
            db.delete(patient)
            db.commit()
            return True, "Data Pasien dan riwayat prediksi berhasil dihapus"
        return False, "Pasien tidak ditemukan"
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}"
    finally:
        db.close()

def get_all_patients():
    db = SessionLocal()
    try:
        patients = db.query(Patient).order_by(Patient.name).all()
        return patients
    finally:
        db.close()

def get_patient_by_id(patient_id):
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        return patient
    finally:
        db.close()

def save_prediction(patient_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, risk_level, model_used):
    db = SessionLocal()
    try:
        record = MaternalRecord(
            patient_id=patient_id,
            age=age,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            bs=bs,
            body_temp=body_temp,
            heart_rate=heart_rate,
            risk_level=risk_level,
            model_used=model_used
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return True, record.id
    except Exception as e:
        db.rollback()
        return False, None
    finally:
        db.close()

def update_prediction(record_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, risk_level, model_used):
    db = SessionLocal()
    try:
        record = db.query(MaternalRecord).filter(MaternalRecord.id == record_id).first()
        if record:
            record.age = age
            record.systolic_bp = systolic_bp
            record.diastolic_bp = diastolic_bp
            record.bs = bs
            record.body_temp = body_temp
            record.heart_rate = heart_rate
            record.risk_level = risk_level
            record.model_used = model_used
            db.commit()
            return True, "Riwayat prediksi berhasil diubah"
        return False, "Riwayat tidak ditemukan"
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}"
    finally:
        db.close()

def delete_prediction(record_id):
    db = SessionLocal()
    try:
        record = db.query(MaternalRecord).filter(MaternalRecord.id == record_id).first()
        if record:
            db.delete(record)
            db.commit()
            return True, "Riwayat prediksi berhasil dihapus"
        return False, "Riwayat tidak ditemukan"
    except Exception as e:
        db.rollback()
        return False, f"Error: {str(e)}"
    finally:
        db.close()

def get_patient_records(patient_id):
    db = SessionLocal()
    try:
        records = db.query(MaternalRecord).filter(MaternalRecord.patient_id == patient_id).order_by(MaternalRecord.created_at.desc()).all()
        return records
    finally:
        db.close()

def get_record_by_id(record_id):
    db = SessionLocal()
    try:
        record = db.query(MaternalRecord).filter(MaternalRecord.id == record_id).first()
        return record
    finally:
        db.close()

def prepare_input_data(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, feature_names):
    input_df = pd.DataFrame({
        'Age': [age],
        'SystolicBP': [systolic_bp],
        'DiastolicBP': [diastolic_bp],
        'BS': [bs],
        'BodyTemp': [body_temp],
        'HeartRate': [heart_rate]
    })
    return input_df[feature_names]

st.title("Sistem Klasifikasi Risiko Kesehatan Maternal")

menu_options = ["Prediksi Risiko", "Kelola Data Pasien", "Riwayat Prediksi"]
menu = st.sidebar.radio("Menu", menu_options)

if menu == "Prediksi Risiko":
    st.header("Prediksi Risiko Kesehatan Maternal")
    
    dt_data, rf_data = load_models()
    dt_model = dt_data["model"]
    rf_model = rf_data["model"]
    label_mapping = dt_data.get("label_mapping", {})
    feature_names = dt_data.get("feature_names") or dt_data.get("feature_order")
    if feature_names is None:
        feature_names = [
            "Age",
            "SystolicBP",
            "DiastolicBP",
            "BS",
            "BodyTemp",
            "HeartRate",
        ]
    
    st.subheader("Data Pasien")
    
    preselect_label_pred = None
    if st.session_state.get("after_save_patient_pred"):
        preselect_label_pred = st.session_state.get("new_patient_label_pred")
        st.session_state.pop("patient_option_pred", None)
        st.session_state.pop("select_patient_prediction", None)
        st.session_state["after_save_patient_pred"] = False

    patients = get_all_patients()
    
    patient_option = st.radio(
        "Pilih Pasien",
        ["Pilih dari data yang ada", "Tambah pasien baru"],
        horizontal=True,
        key="patient_option_pred"
    )
    
    selected_patient_id = None
    
    if patient_option == "Pilih dari data yang ada":
        if patients:
            patient_dict = {f"{p.name} - {p.phone_number}": p.id for p in patients}
            patient_options_list = list(patient_dict.keys())
            if preselect_label_pred and preselect_label_pred in patient_options_list:
                st.session_state["select_patient_prediction"] = preselect_label_pred
            selected_patient = st.selectbox(
                "Pilih Pasien",
                options=patient_options_list,
                key="select_patient_prediction"
            )
            selected_patient_id = patient_dict[selected_patient]
            
            patient_info = get_patient_by_id(selected_patient_id)
            if patient_info:
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**Nama:** {patient_info.name}")
                    st.write(f"**No. Telepon:** {patient_info.phone_number}")
                with col_info2:
                    st.write(f"**Email:** {patient_info.email}")
                    st.write(f"**Alamat:** {patient_info.address}")
        else:
            st.warning("Belum ada data pasien. Silakan tambah pasien baru.")
            patient_option = "Tambah pasien baru"
    
    if patient_option == "Tambah pasien baru":
        st.subheader("Form Pasien Baru")
        col_patient1, col_patient2 = st.columns(2)
        
        with col_patient1:
            new_name = st.text_input("Nama Lengkap", key="new_name_pred")
            new_phone = st.text_input("No. Telepon", key="new_phone_pred")
        
        with col_patient2:
            new_email = st.text_input("Email", key="new_email_pred")
            new_address = st.text_area("Alamat", key="new_address_pred")
        
        if st.button("Simpan Data Pasien", key="save_patient_pred"):
            if new_name and new_phone and new_email and new_address:
                success, message, patient_id = create_patient(new_name, new_email, new_phone, new_address)
                if success:
                    st.success(message)
                    st.session_state["after_save_patient_pred"] = True
                    st.session_state["new_patient_label_pred"] = f"{new_name} - {new_phone}"
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Mohon isi semua field pasien")
    
    st.divider()
    st.subheader("Data Kesehatan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Umur (tahun)", min_value=10, max_value=100, value=25, key="age_pred")
        systolic_bp = st.number_input("Tekanan Darah Sistolik (mmHg)", min_value=70, max_value=200, value=120, key="systolic_pred")
        diastolic_bp = st.number_input("Tekanan Darah Diastolik (mmHg)", min_value=40, max_value=130, value=80, key="diastolic_pred")
    
    with col2:
        bs = st.number_input("Gula Darah (mmol/L)", min_value=0.0, max_value=30.0, value=7.5, step=0.1, key="bs_pred")
        body_temp = st.number_input("Suhu Tubuh (°C)", min_value=34.0, max_value=42.0, value=37.0, step=0.1, key="body_temp_pred")
        heart_rate = st.number_input("Detak Jantung (bpm)", min_value=40, max_value=150, value=75, key="heart_rate_pred")
    
    model_choice = st.selectbox("Pilih Model", ["Decision Tree", "Random Forest"], key="model_choice_pred")
    
    if st.button("Prediksi Risiko", key="btn_predict"):
        if selected_patient_id is None and patient_option == "Pilih dari data yang ada":
            st.error("Mohon pilih pasien terlebih dahulu")
        elif selected_patient_id is None and patient_option == "Tambah pasien baru":
            st.error("Mohon simpan data pasien terlebih dahulu")
        else:
            input_data = prepare_input_data(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, feature_names)
            
            if model_choice == "Decision Tree":
                prediction = dt_model.predict(input_data)
                model_used = "Decision Tree"
            else:
                prediction = rf_model.predict(input_data)
                model_used = "Random Forest"
            
            risk_level = label_mapping[prediction[0]]
            
            st.success(f"Hasil Prediksi: **{risk_level}**")
            
            if risk_level == "Low Risk":
                st.info("Tingkat risiko rendah. Tetap jaga kesehatan dengan pola hidup sehat.")
            elif risk_level == "Mid Risk":
                st.warning("Tingkat risiko menengah. Disarankan untuk konsultasi dengan dokter.")
            else:
                st.error("Tingkat risiko tinggi. Segera konsultasi dengan dokter spesialis.")
            
            success, record_id = save_prediction(selected_patient_id, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, risk_level, model_used)
            if success:
                st.success("Hasil prediksi telah disimpan ke database")
            else:
                st.error("Gagal menyimpan hasil prediksi")

elif menu == "Kelola Data Pasien":
    st.header("Kelola Data Pasien")
    
    preselect_label_manage = None
    if st.session_state.get("after_save_patient_manage"):
        preselect_label_manage = st.session_state.get("new_patient_label_manage")
        st.session_state.pop("manage_option", None)
        st.session_state.pop("select_patient_manage", None)
        st.session_state["after_save_patient_manage"] = False

    manage_option = st.radio(
        "Pilihan",
        ["Tampilkan Data Pasien", "Tambah Pasien Baru"],
        horizontal=True,
        key="manage_option"
    )
    
    if manage_option == "Tambah Pasien Baru":
        st.subheader("Form Tambah Pasien")
        col_patient1, col_patient2 = st.columns(2)
        
        with col_patient1:
            new_name_manage = st.text_input("Nama Lengkap", key="new_name_manage")
            new_phone_manage = st.text_input("No. Telepon", key="new_phone_manage")
        
        with col_patient2:
            new_email_manage = st.text_input("Email", key="new_email_manage")
            new_address_manage = st.text_area("Alamat", key="new_address_manage")
        
        if st.button("Simpan Data Pasien", key="save_patient_manage"):
            if new_name_manage and new_phone_manage and new_email_manage and new_address_manage:
                success, message, patient_id = create_patient(new_name_manage, new_email_manage, new_phone_manage, new_address_manage)
                if success:
                    st.success(message)
                    st.session_state["after_save_patient_manage"] = True
                    st.session_state["new_patient_label_manage"] = f"{new_name_manage} - {new_phone_manage}"
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Mohon isi semua field pasien")
    
    else:
        patients = get_all_patients()
        
        if patients:
            patient_dict = {f"{p.name} - {p.phone_number}": p.id for p in patients}
            patient_options_list = list(patient_dict.keys())
            if preselect_label_manage and preselect_label_manage in patient_options_list:
                st.session_state["select_patient_manage"] = preselect_label_manage
            selected_patient = st.selectbox(
                "Pilih Pasien",
                options=patient_options_list,
                key="select_patient_manage"
            )
            selected_patient_id = patient_dict[selected_patient]
            
            patient_info = get_patient_by_id(selected_patient_id)
            if patient_info:
                st.subheader(f"Data Pasien: {patient_info.name}")
                
                col_action1, col_action2, col_action3 = st.columns(3)
                
                with col_action1:
                    if st.button("Ubah Data", key=f"btn_edit_{selected_patient_id}"):
                        st.session_state.edit_mode = True
                
                with col_action2:
                    if st.button("Hapus Data", key=f"btn_delete_{selected_patient_id}"):
                        success, message = delete_patient(selected_patient_id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                
                if st.session_state.get("edit_mode"):
                    st.divider()
                    st.subheader("Ubah Data Pasien")
                    col_edit1, col_edit2 = st.columns(2)
                    
                    with col_edit1:
                        edit_name = st.text_input("Nama Lengkap", value=patient_info.name, key="edit_name")
                        edit_phone = st.text_input("No. Telepon", value=patient_info.phone_number, key="edit_phone")
                    
                    with col_edit2:
                        edit_email = st.text_input("Email", value=patient_info.email, key="edit_email")
                        edit_address = st.text_area("Alamat", value=patient_info.address, key="edit_address")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("Simpan Perubahan", key="btn_save_edit"):
                            success, message = update_patient(selected_patient_id, edit_name, edit_email, edit_phone, edit_address)
                            if success:
                                st.success(message)
                                st.session_state.edit_mode = False
                                st.rerun()
                            else:
                                st.error(message)
                    
                    with col_btn2:
                        if st.button("Batal", key="btn_cancel_edit"):
                            st.session_state.edit_mode = False
                            st.rerun()
                
                else:
                    st.divider()
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Nama:** {patient_info.name}")
                        st.write(f"**No. Telepon:** {patient_info.phone_number}")
                    with col_info2:
                        st.write(f"**Email:** {patient_info.email}")
                        st.write(f"**Alamat:** {patient_info.address}")
        else:
            st.info("Belum ada data pasien")

elif menu == "Riwayat Prediksi":
    st.header("Riwayat Prediksi")
    
    patients = get_all_patients()
    
    if patients:
        patient_dict = {f"{p.name} - {p.phone_number}": p.id for p in patients}
        selected_patient = st.selectbox(
            "Pilih Pasien",
            options=list(patient_dict.keys()),
            key="select_patient_history"
        )
        selected_patient_id = patient_dict[selected_patient]
        
        patient_info = get_patient_by_id(selected_patient_id)
        if patient_info:
            st.subheader(f"Data Pasien: {patient_info.name}")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**No. Telepon:** {patient_info.phone_number}")
                st.write(f"**Email:** {patient_info.email}")
            with col_info2:
                st.write(f"**Alamat:** {patient_info.address}")
            
            st.divider()
            
            records = get_patient_records(selected_patient_id)
            
            if records:
                st.subheader("Daftar Riwayat Prediksi")
                
                for idx, record in enumerate(records):
                    with st.expander(f"Prediksi {idx + 1} - {record.created_at.strftime('%Y-%m-%d %H:%M')} - {record.risk_level}", expanded=False):
                        col_rec1, col_rec2 = st.columns(2)
                        with col_rec1:
                            st.write(f"**Umur:** {record.age} tahun")
                            st.write(f"**Tekanan Darah:** {record.systolic_bp}/{record.diastolic_bp} mmHg")
                            st.write(f"**Gula Darah:** {record.bs} mmol/L")
                        with col_rec2:
                            st.write(f"**Suhu Tubuh:** {record.body_temp} °C")
                            st.write(f"**Detak Jantung:** {record.heart_rate} bpm")
                            st.write(f"**Model:** {record.model_used}")
                        
                        st.write(f"**Tingkat Risiko:** {record.risk_level}")
                        
                        col_action1, col_action2, col_action3 = st.columns(3)
                        
                        with col_action1:
                            if st.button("Ubah", key=f"btn_edit_record_{record.id}"):
                                st.session_state[f"edit_record_{record.id}"] = True
                        
                        with col_action2:
                            if st.button("Hapus", key=f"btn_delete_record_{record.id}"):
                                success, message = delete_prediction(record.id)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                        
                        if st.session_state.get(f"edit_record_{record.id}"):
                            st.divider()
                            st.write("**Ubah Data Prediksi**")
                            
                            col_edit1, col_edit2 = st.columns(2)
                            with col_edit1:
                                edit_age = st.number_input("Umur (tahun)", min_value=10, max_value=100, value=record.age, key=f"edit_age_{record.id}")
                                edit_systolic = st.number_input("Tekanan Darah Sistolik (mmHg)", min_value=70, max_value=200, value=record.systolic_bp, key=f"edit_systolic_{record.id}")
                                edit_diastolic = st.number_input("Tekanan Darah Diastolik (mmHg)", min_value=40, max_value=130, value=record.diastolic_bp, key=f"edit_diastolic_{record.id}")
                            
                            with col_edit2:
                                edit_bs = st.number_input("Gula Darah (mmol/L)", min_value=0.0, max_value=30.0, value=record.bs, step=0.1, key=f"edit_bs_{record.id}")
                                edit_body_temp = st.number_input("Suhu Tubuh (°C)", min_value=34.0, max_value=42.0, value=record.body_temp, step=0.1, key=f"edit_body_temp_{record.id}")
                                edit_heart_rate = st.number_input("Detak Jantung (bpm)", min_value=40, max_value=150, value=record.heart_rate, key=f"edit_heart_rate_{record.id}")
                            
                            edit_model = st.selectbox("Pilih Model", ["Decision Tree", "Random Forest"], index=0 if record.model_used == "Decision Tree" else 1, key=f"edit_model_{record.id}")
                            
                            if st.button("Prediksi Ulang & Simpan", key=f"btn_save_edit_record_{record.id}"):
                                dt_data, rf_data = load_models()
                                dt_model_edit = dt_data["model"]
                                rf_model_edit = rf_data["model"]
                                label_mapping_edit = dt_data["label_mapping"]
                                feature_names_edit = dt_data["feature_names"]
                                
                                input_data = prepare_input_data(edit_age, edit_systolic, edit_diastolic, edit_bs, edit_body_temp, edit_heart_rate, feature_names_edit)
                                
                                if edit_model == "Decision Tree":
                                    new_prediction = dt_model_edit.predict(input_data)
                                else:
                                    new_prediction = rf_model_edit.predict(input_data)
                                
                                new_risk_level = label_mapping_edit[new_prediction[0]]
                                
                                success, message = update_prediction(record.id, edit_age, edit_systolic, edit_diastolic, edit_bs, edit_body_temp, edit_heart_rate, new_risk_level, edit_model)
                                
                                if success:
                                    st.success(f"Data berhasil diubah. Prediksi baru: {new_risk_level}")
                                    st.session_state[f"edit_record_{record.id}"] = False
                                    st.rerun()
                                else:
                                    st.error(message)
                            
                            if st.button("Batal", key=f"btn_cancel_edit_record_{record.id}"):
                                st.session_state[f"edit_record_{record.id}"] = False
                                st.rerun()
                
                st.divider()
                st.subheader("Statistik Risiko")
                
                data = []
                for record in records:
                    data.append({
                        "Tingkat Risiko": record.risk_level
                    })
                
                df = pd.DataFrame(data)
                risk_counts = df['Tingkat Risiko'].value_counts()
                st.bar_chart(risk_counts)
            else:
                st.info("Belum ada riwayat prediksi untuk pasien ini")
    else:
        st.info("Belum ada data pasien")

if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False

if "show_error_modal" not in st.session_state:
    st.session_state.show_error_modal = False

if "show_success_modal_manage" not in st.session_state:
    st.session_state.show_success_modal_manage = False

if "show_error_modal_manage" not in st.session_state:
    st.session_state.show_error_modal_manage = False

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False