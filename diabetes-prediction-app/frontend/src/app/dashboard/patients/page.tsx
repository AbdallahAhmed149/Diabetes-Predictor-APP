'use client';

import { useState, useEffect } from 'react';
import { patientsAPI } from '@/lib/api';

interface Patient {
    id: number;
    patient_code: string;
    user_id?: number;
    date_of_birth?: string;
    phone?: string;
    address?: string;
    emergency_contact?: string;
    created_at: string;
}

export default function PatientsPage() {
    const [patients, setPatients] = useState<Patient[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
    const [formData, setFormData] = useState({
        patient_code: '',
        date_of_birth: '',
        phone: '',
        address: '',
        emergency_contact: ''
    });

    useEffect(() => {
        fetchPatients();
    }, []);

    const fetchPatients = async () => {
        try {
            setLoading(true);
            const response = await patientsAPI.list();
            setPatients(response.data);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load patients');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (editingPatient) {
                await patientsAPI.update(editingPatient.id, formData);
            } else {
                await patientsAPI.create(formData);
            }
            setShowModal(false);
            resetForm();
            fetchPatients();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this patient?')) return;
        try {
            await patientsAPI.delete(id);
            fetchPatients();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Delete failed');
        }
    };

    const handleEdit = (patient: Patient) => {
        setEditingPatient(patient);
        setFormData({
            patient_code: patient.patient_code,
            date_of_birth: patient.date_of_birth || '',
            phone: patient.phone || '',
            address: patient.address || '',
            emergency_contact: patient.emergency_contact || ''
        });
        setShowModal(true);
    };

    const resetForm = () => {
        setFormData({
            patient_code: '',
            date_of_birth: '',
            phone: '',
            address: '',
            emergency_contact: ''
        });
        setEditingPatient(null);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        resetForm();
    };

    if (loading) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <p>Loading patients...</p>
            </div>
        );
    }

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>👥 Patient Management</h1>
                <button
                    className="btn btn-primary"
                    onClick={() => setShowModal(true)}
                >
                    + Add Patient
                </button>
            </div>

            {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

            <div className="card">
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ borderBottom: '2px solid var(--border)' }}>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Patient Code</th>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Date of Birth</th>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Phone</th>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Emergency Contact</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {patients.length === 0 ? (
                            <tr>
                                <td colSpan={5} style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                    No patients found. Add your first patient to get started!
                                </td>
                            </tr>
                        ) : (
                            patients.map((patient) => (
                                <tr key={patient.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem' }}>{patient.patient_code}</td>
                                    <td style={{ padding: '1rem' }}>{patient.date_of_birth || 'N/A'}</td>
                                    <td style={{ padding: '1rem' }}>{patient.phone || 'N/A'}</td>
                                    <td style={{ padding: '1rem' }}>{patient.emergency_contact || 'N/A'}</td>
                                    <td style={{ padding: '1rem', textAlign: 'center' }}>
                                        <button
                                            className="btn btn-secondary"
                                            style={{ marginRight: '0.5rem', padding: '0.5rem 1rem' }}
                                            onClick={() => handleEdit(patient)}
                                        >
                                            Edit
                                        </button>
                                        <button
                                            className="btn"
                                            style={{ padding: '0.5rem 1rem', background: '#dc3545', color: 'white' }}
                                            onClick={() => handleDelete(patient.id)}
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Modal */}
            {showModal && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0,0,0,0.5)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 1000
                }}>
                    <div className="card" style={{ width: '500px', maxWidth: '90%' }}>
                        <h2 style={{ marginBottom: '1.5rem' }}>
                            {editingPatient ? 'Edit Patient' : 'Add New Patient'}
                        </h2>
                        <form onSubmit={handleSubmit}>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Patient Code *</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.patient_code}
                                    onChange={(e) => setFormData({ ...formData, patient_code: e.target.value })}
                                    required
                                    disabled={!!editingPatient}
                                    placeholder="e.g., P001"
                                />
                            </div>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Date of Birth</label>
                                <input
                                    type="date"
                                    className="input"
                                    value={formData.date_of_birth}
                                    onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                                />
                            </div>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Phone</label>
                                <input
                                    type="tel"
                                    className="input"
                                    value={formData.phone}
                                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                    placeholder="+1 234 567 8900"
                                />
                            </div>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Address</label>
                                <textarea
                                    className="input"
                                    value={formData.address}
                                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                                    rows={2}
                                    placeholder="Enter address"
                                />
                            </div>
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Emergency Contact</label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.emergency_contact}
                                    onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
                                    placeholder="Name and phone"
                                />
                            </div>
                            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                                <button
                                    type="button"
                                    className="btn btn-secondary"
                                    onClick={handleCloseModal}
                                >
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn-primary">
                                    {editingPatient ? 'Update' : 'Create'} Patient
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
