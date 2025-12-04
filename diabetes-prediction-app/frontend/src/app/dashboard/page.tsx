'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { removeAuthCookie } from '@/lib/auth';
import { authAPI } from '@/lib/api';

export default function DashboardPage() {
    const [user, setUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUser();
    }, []);

    const fetchUser = async () => {
        try {
            const response = await authAPI.getMe();
            setUser(response.data);
        } catch (err) {
            console.error('Failed to fetch user');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        removeAuthCookie();
        window.location.href = '/login';
    };

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{
                maxWidth: '1200px',
                margin: '0 auto'
            }}>
                {/* Beautiful Welcome Header */}
                {!loading && user && (
                    <div style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        borderRadius: '16px',
                        padding: '1.25rem 1.5rem',
                        marginBottom: '1.5rem',
                        boxShadow: '0 8px 30px rgba(102, 126, 234, 0.25)',
                        color: 'white',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                    }}>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '1.5rem'
                        }}>
                            <div>
                                <span style={{
                                    fontSize: '0.9rem',
                                    opacity: 0.85,
                                    marginRight: '0.5rem'
                                }}>
                                    Welcome back,
                                </span>
                                <span style={{
                                    fontSize: '1.5rem',
                                    fontWeight: 'bold'
                                }}>
                                    {user.full_name}
                                </span>
                            </div>
                            <span style={{
                                padding: '0.4rem 1.2rem',
                                borderRadius: '25px',
                                background: user.role === 'doctor'
                                    ? 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'
                                    : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                                fontSize: '0.85rem',
                                fontWeight: '600',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px',
                                boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                            }}>
                                {user.role === 'doctor' ? '👨‍⚕️ Doctor' : '👤 Patient'}
                            </span>
                        </div>
                        <button onClick={handleLogout} className="btn" style={{
                            background: 'rgba(255, 255, 255, 0.2)',
                            backdropFilter: 'blur(10px)',
                            border: '2px solid rgba(255, 255, 255, 0.3)',
                            color: 'white',
                            fontWeight: '600',
                            padding: '0.5rem 1.2rem',
                            fontSize: '0.9rem'
                        }}>
                            🚪 Logout
                        </button>
                    </div>
                )}

                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '2rem'
                }}>
                    <h1 style={{ fontSize: '2rem' }}>🩺 Diabetes Prediction Dashboard</h1>
                </div>

                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                    gap: '1.5rem',
                    marginBottom: '2rem'
                }}>
                    <div className="card" style={{ textAlign: 'center' }}>
                        <h2 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>📊 New Prediction</h2>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                            Create a new diabetes risk assessment
                        </p>
                        <Link href="/dashboard/predict" className="btn btn-primary" style={{ textDecoration: 'none' }}>
                            Start Assessment
                        </Link>
                    </div>


                    {/* Patients card - Only visible for doctors */}
                    {user && user.role === 'doctor' && (
                        <div className="card" style={{ textAlign: 'center' }}>
                            <h2 style={{ color: 'var(--secondary)', marginBottom: '1rem' }}>👥 Patients</h2>
                            <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                                Manage patient profiles and records
                            </p>
                            <Link href="/dashboard/patients" className="btn btn-secondary" style={{ textDecoration: 'none' }}>
                                View Patients
                            </Link>
                        </div>
                    )}

                    <div className="card" style={{ textAlign: 'center' }}>
                        <h2 style={{ color: 'var(--accent)', marginBottom: '1rem' }}>📝 History</h2>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                            View past predictions and trends
                        </p>
                        <Link href="/dashboard/history" className="btn btn-accent" style={{ textDecoration: 'none' }}>
                            View History
                        </Link>
                    </div>
                </div>

                <div className="card">
                    <h2 style={{ marginBottom: '1rem' }}>🚀 Quick Start Guide</h2>
                    <ol style={{ lineHeight: '2', color: 'var(--text-secondary)', paddingLeft: '1.5rem' }}>
                        {user && user.role === 'doctor' ? (
                            <>
                                <li>Create or select a patient profile</li>
                                <li>Complete the comprehensive health assessment form (29 fields)</li>
                                <li>Review the AI-powered risk prediction results</li>
                                <li>Download PDF reports for clinical records</li>
                                <li>Track predictions over time to monitor health trends</li>
                            </>
                        ) : (
                            <>
                                <li>Click "Start Assessment" to check your diabetes risk</li>
                                <li>Fill out your health information accurately</li>
                                <li>Review your personalized risk assessment</li>
                                <li>Download your report for your records</li>
                                <li>Track your progress in the History section</li>
                            </>
                        )}
                    </ol>
                </div>
            </div>
        </div>
    );
}
