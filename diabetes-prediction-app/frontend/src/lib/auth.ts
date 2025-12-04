// Set auth cookie for middleware
export function setAuthCookie(token: string) {
    document.cookie = `access_token=${token}; path=/; max-age=${60 * 60 * 24 * 7}`; // 7 days
    localStorage.setItem('access_token', token);
}

// Remove auth cookie
export function removeAuthCookie() {
    document.cookie = 'access_token=; path=/; max-age=0';
    localStorage.removeItem('access_token');
}

// Get auth token
export function getAuthToken(): string | null {
    return localStorage.getItem('access_token');
}
