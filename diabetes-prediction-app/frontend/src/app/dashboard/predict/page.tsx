'use client';

import { useState, useEffect } from 'react';
import { predictionsAPI, patientsAPI, authAPI } from '@/lib/api';

interface Patient {
    id: number;
    patient_code: string;
}

interface PredictionResult {
    id: number;
    risk_probability: number;
    risk_level: string;
    risk_interpretation: string;
}

export default function PredictPage() {
    const [patients, setPatients] = useState<Patient[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [result, setResult] = useState<PredictionResult | null>(null);
    const [userRole, setUserRole] = useState<string>('');
    const [loadingUserRole, setLoadingUserRole] = useState(true);

    const [formData, setFormData] = useState({
        patient_id: '',
        // Demographics
        age: '',
        gender: 'Male',
        ethnicity: 'Other',
        education_level: 'Highschool',
        income_level: 'Middle',
        employment_status: 'Employed',
        // Lifestyle
        smoking_status: 'Never',
        alcohol_consumption_per_week: '',
        physical_activity_minutes_per_week: '',
        diet_score: '',
        sleep_hours_per_day: '',
        screen_time_hours_per_day: '',
        // Medical History
        family_history_diabetes: false,
        hypertension_history: false,
        cardiovascular_history: false,
        // Physical Measurements
        bmi: '',
        waist_to_hip_ratio: '',
        systolic_bp: '',
        diastolic_bp: '',
        heart_rate: '',
        // Lab Results
        cholesterol_total: '',
        hdl_cholesterol: '',
        ldl_cholesterol: '',
        triglycerides: '',
        glucose_fasting: '',
        glucose_postprandial: '',
        insulin_level: '',
        hba1c: '',
        diabetes_risk_score: ''
    });

    useEffect(() => {
        fetchUserAndPatients();
    }, []);

    const fetchUserAndPatients = async () => {
        try {
            setLoadingUserRole(true);
            // First fetch user to get role
            const userResponse = await authAPI.getMe();
            const role = userResponse.data.role;
            setUserRole(role);

            // Then fetch patients
            const patientsResponse = await patientsAPI.list();
            setPatients(patientsResponse.data);

            // For patients, auto-select their patient_id
            if (role === 'patient' && patientsResponse.data.length > 0) {
                setFormData(prev => ({
                    ...prev,
                    patient_id: patientsResponse.data[0].id.toString()
                }));
            }
        } catch (err) {
            console.error('Failed to load data');
        } finally {
            setLoadingUserRole(false);
        }
    };



    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess(false);
        setResult(null);
        setLoading(true);

        try {
            const payload = {
                patient_id: parseInt(formData.patient_id),
                age: parseInt(formData.age),
                gender: formData.gender,
                bmi: parseFloat(formData.bmi),
                systolic_bp: parseInt(formData.systolic_bp),
                diastolic_bp: parseInt(formData.diastolic_bp),
                glucose_fasting: parseFloat(formData.glucose_fasting),
                cholesterol_total: parseFloat(formData.cholesterol_total),
                hdl_cholesterol: parseFloat(formData.hdl_cholesterol),
                smoking_status: formData.smoking_status,
                physical_activity_minutes_per_week: parseInt(formData.physical_activity_minutes_per_week),
                family_history_diabetes: formData.family_history_diabetes,
                hypertension_history: formData.hypertension_history,
                // Additional comprehensive fields
                ethnicity: formData.ethnicity,
                education_level: formData.education_level,
                income_level: formData.income_level,
                employment_status: formData.employment_status,
                alcohol_consumption_per_week: parseFloat(formData.alcohol_consumption_per_week || '0'),
                diet_score: parseFloat(formData.diet_score || '5'),
                sleep_hours_per_day: parseFloat(formData.sleep_hours_per_day || '7'),
                screen_time_hours_per_day: parseFloat(formData.screen_time_hours_per_day || '4'),
                cardiovascular_history: formData.cardiovascular_history,
                waist_to_hip_ratio: parseFloat(formData.waist_to_hip_ratio || '0.85'),
                heart_rate: parseInt(formData.heart_rate || '70'),
                ldl_cholesterol: parseFloat(formData.ldl_cholesterol || '100'),
                triglycerides: parseFloat(formData.triglycerides || '150'),
                glucose_postprandial: parseFloat(formData.glucose_postprandial || '120'),
                insulin_level: parseFloat(formData.insulin_level || '10'),
                hba1c: parseFloat(formData.hba1c || '5.5'),
                diabetes_risk_score: parseFloat(formData.diabetes_risk_score || '0')
            };

            const response = await predictionsAPI.create(payload);
            setResult(response.data);
            setSuccess(true);
        } catch (err: any) {
            let errorMessage = 'Prediction failed. Please try again.';
            if (err.response?.data) {
                const data = err.response.data;
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMessage = data.detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ');
                }
            }
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (level: string) => {
        switch (level?.toLowerCase()) {
            case 'low': return '#28a745';
            case 'medium': return '#ffc107';
            case 'high': return '#dc3545';
            default: return '#6c757d';
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2rem' }}>
                <span style={{ fontSize: '3rem', marginRight: '1rem' }}>📊</span>
                <h1 style={{ margin: 0 }}>Diabetes Risk Assessment</h1>
            </div>

            {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

            {success && result && (
                <div className="card" style={{
                    marginBottom: '2rem',
                    padding: '2rem',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white'
                }}>
                    <h2 style={{ marginBottom: '1rem', color: 'white' }}>✅ Prediction Complete</h2>
                    <div style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                        {result.risk_probability.toFixed(1)}%
                    </div>
                    <div style={{
                        fontSize: '1.5rem',
                        padding: '0.5rem 1rem',
                        background: getRiskColor(result.risk_level),
                        borderRadius: '8px',
                        display: 'inline-block',
                        marginBottom: '1rem'
                    }}>
                        {result.risk_level} Risk
                    </div>
                    <p style={{ fontSize: '1.1rem', lineHeight: '1.6', opacity: 0.95 }}>
                        {result.risk_interpretation}
                    </p>
                </div>
            )}

            {loadingUserRole ? (
                <div className="card" style={{ padding: '3rem', textAlign: 'center' }}>
                    <p>Loading...</p>
                </div>
            ) : (
                <div className="card">
                    <form onSubmit={handleSubmit}>
                        {/* Patient selection - only shown to doctors */}
                        {userRole === 'doctor' && (
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                    Select Patient *
                                </label>
                                <select
                                    className="input"
                                    value={formData.patient_id}
                                    onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
                                    required
                                >
                                    <option value="">Choose a patient...</option>
                                    {patients.map(p => (
                                        <option key={p.id} value={p.id}>
                                            {p.patient_code}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        )}

                        <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>👤 Demographics</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Age *</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.age}
                                    onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                                    required
                                    min="18"
                                    max="120"
                                    placeholder="35"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Gender *</label>
                                <select
                                    className="input"
                                    value={formData.gender}
                                    onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                                >
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ethnicity</label>
                                <select
                                    className="input"
                                    value={formData.ethnicity}
                                    onChange={(e) => setFormData({ ...formData, ethnicity: e.target.value })}
                                >
                                    <option value="White">White</option>
                                    <option value="Black">Black</option>
                                    <option value="Asian">Asian</option>
                                    <option value="Hispanic">Hispanic</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Education Level</label>
                                <select
                                    className="input"
                                    value={formData.education_level}
                                    onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
                                >
                                    <option value="No formal">No formal</option>
                                    <option value="Highschool">High School</option>
                                    <option value="Graduate">Graduate</option>
                                    <option value="Postgraduate">Postgraduate</option>
                                </select>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Income Level</label>
                                <select
                                    className="input"
                                    value={formData.income_level}
                                    onChange={(e) => setFormData({ ...formData, income_level: e.target.value })}
                                >
                                    <option value="Low">Low</option>
                                    <option value="Lower-Middle">Lower-Middle</option>
                                    <option value="Middle">Middle</option>
                                    <option value="Upper-Middle">Upper-Middle</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Employment Status</label>
                                <select
                                    className="input"
                                    value={formData.employment_status}
                                    onChange={(e) => setFormData({ ...formData, employment_status: e.target.value })}
                                >
                                    <option value="Employed">Employed</option>
                                    <option value="Unemployed">Unemployed</option>
                                    <option value="Retired">Retired</option>
                                    <option value="Student">Student</option>
                                </select>
                            </div>
                        </div>

                        <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>📏 Physical Measurements</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>BMI *</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.bmi}
                                    onChange={(e) => setFormData({ ...formData, bmi: e.target.value })}
                                    required
                                    placeholder="25.5"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Waist-Hip Ratio</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    className="input"
                                    value={formData.waist_to_hip_ratio}
                                    onChange={(e) => setFormData({ ...formData, waist_to_hip_ratio: e.target.value })}
                                    placeholder="0.85"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Heart Rate (bpm)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.heart_rate}
                                    onChange={(e) => setFormData({ ...formData, heart_rate: e.target.value })}
                                    placeholder="70"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Systolic BP *</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.systolic_bp}
                                    onChange={(e) => setFormData({ ...formData, systolic_bp: e.target.value })}
                                    required
                                    placeholder="120"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Diastolic BP *</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.diastolic_bp}
                                    onChange={(e) => setFormData({ ...formData, diastolic_bp: e.target.value })}
                                    required
                                    placeholder="80"
                                />
                            </div>
                        </div>

                        <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>🩺 Lab Results</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Fasting Glucose *</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.glucose_fasting}
                                    onChange={(e) => setFormData({ ...formData, glucose_fasting: e.target.value })}
                                    required
                                    placeholder="95"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Postprandial Glucose</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.glucose_postprandial}
                                    onChange={(e) => setFormData({ ...formData, glucose_postprandial: e.target.value })}
                                    placeholder="120"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>HbA1c (%)</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.hba1c}
                                    onChange={(e) => setFormData({ ...formData, hba1c: e.target.value })}
                                    placeholder="5.5"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Insulin Level</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.insulin_level}
                                    onChange={(e) => setFormData({ ...formData, insulin_level: e.target.value })}
                                    placeholder="10"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Total Cholesterol *</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.cholesterol_total}
                                    onChange={(e) => setFormData({ ...formData, cholesterol_total: e.target.value })}
                                    required
                                    placeholder="200"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>HDL Cholesterol *</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.hdl_cholesterol}
                                    onChange={(e) => setFormData({ ...formData, hdl_cholesterol: e.target.value })}
                                    required
                                    placeholder="50"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>LDL Cholesterol</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.ldl_cholesterol}
                                    onChange={(e) => setFormData({ ...formData, ldl_cholesterol: e.target.value })}
                                    placeholder="100"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Triglycerides</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.triglycerides}
                                    onChange={(e) => setFormData({ ...formData, triglycerides: e.target.value })}
                                    placeholder="150"
                                />
                            </div>
                        </div>

                        <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>🏃 Lifestyle Factors</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Smoking Status *</label>
                                <select
                                    className="input"
                                    value={formData.smoking_status}
                                    onChange={(e) => setFormData({ ...formData, smoking_status: e.target.value })}
                                >
                                    <option value="Never">Never</option>
                                    <option value="Former">Former</option>
                                    <option value="Current">Current</option>
                                </select>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Alcohol (drinks/week)</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.alcohol_consumption_per_week}
                                    onChange={(e) => setFormData({ ...formData, alcohol_consumption_per_week: e.target.value })}
                                    placeholder="0"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Physical Activity (min/week) *</label>
                                <input
                                    type="number"
                                    className="input"
                                    value={formData.physical_activity_minutes_per_week}
                                    onChange={(e) => setFormData({ ...formData, physical_activity_minutes_per_week: e.target.value })}
                                    required
                                    placeholder="150"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Diet Score (0-10)</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.diet_score}
                                    onChange={(e) => setFormData({ ...formData, diet_score: e.target.value })}
                                    placeholder="5"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Sleep (hours/day)</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.sleep_hours_per_day}
                                    onChange={(e) => setFormData({ ...formData, sleep_hours_per_day: e.target.value })}
                                    placeholder="7"
                                />
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Screen Time (hours/day)</label>
                                <input
                                    type="number"
                                    step="0.1"
                                    className="input"
                                    value={formData.screen_time_hours_per_day}
                                    onChange={(e) => setFormData({ ...formData, screen_time_hours_per_day: e.target.value })}
                                    placeholder="4"
                                />
                            </div>
                        </div>

                        <h3 style={{ marginBottom: '1rem', color: 'var(--primary)' }}>🏥 Medical History</h3>
                        <div style={{ marginBottom: '2rem', display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.5rem' }}>
                            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                                <input
                                    type="checkbox"
                                    checked={formData.family_history_diabetes}
                                    onChange={(e) => setFormData({ ...formData, family_history_diabetes: e.target.checked })}
                                    style={{ marginRight: '0.5rem', width: '20px', height: '20px' }}
                                />
                                Family History of Diabetes
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                                <input
                                    type="checkbox"
                                    checked={formData.hypertension_history}
                                    onChange={(e) => setFormData({ ...formData, hypertension_history: e.target.checked })}
                                    style={{ marginRight: '0.5rem', width: '20px', height: '20px' }}
                                />
                                History of Hypertension
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                                <input
                                    type="checkbox"
                                    checked={formData.cardiovascular_history}
                                    onChange={(e) => setFormData({ ...formData, cardiovascular_history: e.target.checked })}
                                    style={{ marginRight: '0.5rem', width: '20px', height: '20px' }}
                                />
                                Cardiovascular History
                            </label>
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary"
                            disabled={loading}
                            style={{ width: '100%', padding: '1rem', fontSize: '1.1rem' }}
                        >
                            {loading ? '🔄 Analyzing...' : '🎯 Calculate Risk'}
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
}
