import api from './api';

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export const login = async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post<LoginResponse>('/token', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });

    return response.data;
};

export interface RegisterResponse {
    message: string;
}

export const registerLibrarian = async (username: string, password: string): Promise<RegisterResponse> => {
    const response = await api.post<RegisterResponse>('/register', {
        username,
        password,
    });
    return response.data; 
};

export interface ChangePasswordResponse {
    message: string;
}

export const changePassword = async (newPassword: string, token: string): Promise<ChangePasswordResponse> => {
    const response = await api.put<ChangePasswordResponse>('/passwordchange', {
        newPassword,
    }, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data; 
};