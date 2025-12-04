'use client';

import { useState, useEffect } from 'react';
import { predictionsAPI, authAPI } from '@/lib/api';

interface Prediction {
    id: number;
    patient_id: number;
    risk_probability: number;
    risk_level: string;
    age?: number;
    gender?: string;
    bmi?: number;
    created_at: string;
}

export default function HistoryPage() {
    const [predictions, setPredictions] = useState<Prediction[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [downloading, setDownloading] = useState<number | null>(null);
    const [userRole, setUserRole] = useState<string>('');

    useEffect(() => {
        fetchUserAndHistory();
    }, []);

    const fetchUserAndHistory = async () => {
        try {
            setLoading(true);
            // Fetch user role first
            const userResponse = await authAPI.getMe();
            setUserRole(userResponse.data.role);

            // Then fetch predictions
            const response = await predictionsAPI.list();
            setPredictions(response.data);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load history');
        } finally {
            setLoading(false);
        }
    };

    const fetchHistory = async () => {
        try {
            setLoading(true);
            const response = await predictionsAPI.list();
            setPredictions(response.data);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load history');
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

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const handleDownloadReport = async (predictionId: number) => {
        try {
            setDownloading(predictionId);
            const response = await predictionsAPI.downloadReport(predictionId);

            // Create blob and download
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `diabetes_report_${predictionId}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to download report');
        } finally {
            setDownloading(null);
        }
    };

    if (loading) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <p>Loading prediction history...</p>
            </div>
        );
    }

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>📋 Prediction History</h1>
                <button
                    className="btn btn-secondary"
                    onClick={fetchHistory}
                >
                    🔄 Refresh
                </button>
            </div>

            {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

            <div className="card">
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ borderBottom: '2px solid var(--border)' }}>
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Date</th>
                            {/* Patient ID column - only visible to doctors */}
                            {userRole === 'doctor' && (
                                <th style={{ padding: '1rem', textAlign: 'left' }}>Patient ID</th>
                            )}
                            <th style={{ padding: '1rem', textAlign: 'left' }}>Demographics</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Risk %</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Risk Level</th>
                            <th style={{ padding: '1rem', textAlign: 'center' }}>Report</th>
                        </tr>
                    </thead>
                    <tbody>
                        {predictions.length === 0 ? (
                            <tr>
                                <td colSpan={userRole === 'doctor' ? 6 : 5} style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📊</div>
                                    <p>No predictions yet. Create your first assessment to see results here!</p>
                                </td>
                            </tr>
                        ) : (
                            predictions.map((pred) => (
                                <tr key={pred.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '1rem' }}>
                                        {formatDate(pred.created_at)}
                                    </td>
                                    {/* Patient ID - only visible to doctors */}
                                    {userRole === 'doctor' && (
                                        <td style={{ padding: '1rem' }}>
                                            #{pred.patient_id}
                                        </td>
                                    )}
                                    <td style={{ padding: '1rem' }}>
                                        {pred.age && pred.gender && pred.bmi ? (
                                            <>
                                                {pred.age}y, {pred.gender}, BMI: {pred.bmi.toFixed(1)}
                                            </>
                                        ) : (
                                            'N/A'
                                        )}
                                    </td>
                                    <td style={{ padding: '1rem', textAlign: 'center', fontWeight: 'bold', fontSize: '1.1rem' }}>
                                        {pred.risk_probability.toFixed(1)}%
                                    </td>
                                    <td style={{ padding: '1rem', textAlign: 'center' }}>
                                        <span style={{
                                            padding: '0.5rem 1rem',
                                            borderRadius: '20px',
                                            background: getRiskColor(pred.risk_level),
                                            color: 'white',
                                            fontWeight: '500',
                                            display: 'inline-block',
                                            textTransform: 'uppercase',
                                            fontSize: '0.9rem'
                                        }}>
                                            {pred.risk_level}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem', textAlign: 'center' }}>
                                        <button
                                            className="btn btn-primary btn-sm"
                                            onClick={() => handleDownloadReport(pred.id)}
                                            disabled={downloading === pred.id}
                                            style={{ textDecoration: 'none' }}
                                        >
                                            {downloading === pred.id ? '⏳' : '📄'} Download
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>

                {predictions.length > 0 && (
                    <div style={{
                        marginTop: '1.5rem',
                        padding: '1rem',
                        background: 'var(--surface)',
                        borderRadius: '8px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                    }}>
                        <div>
                            <strong>Total Predictions:</strong> {predictions.length}
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9rem' }}>
                            <div>
                                <span style={{
                                    display: 'inline-block',
                                    width: '12px',
                                    height: '12px',
                                    background: '#28a745',
                                    borderRadius: '50%',
                                    marginRight: '0.5rem'
                                }}></span>
                                Low Risk: {predictions.filter(p => p.risk_level.toLowerCase() === 'low').length}
                            </div>
                            <div>
                                <span style={{
                                    display: 'inline-block',
                                    width: '12px',
                                    height: '12px',
                                    background: '#ffc107',
                                    borderRadius: '50%',
                                    marginRight: '0.5rem'
                                }}></span>
                                Medium Risk: {predictions.filter(p => p.risk_level.toLowerCase() === 'medium').length}
                            </div>
                            <div>
                                <span style={{
                                    display: 'inline-block',
                                    width: '12px',
                                    height: '12px',
                                    background: '#dc3545',
                                    borderRadius: '50%',
                                    marginRight: '0.5rem'
                                }}></span>
                                High Risk: {predictions.filter(p => p.risk_level.toLowerCase() === 'high').length}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {predictions.length > 0 && (
                <div style={{ marginTop: '1.5rem', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    <p>💡 Tip: Click refresh to load the latest predictions</p>
                </div>
            )}
        </div>
    );
}
