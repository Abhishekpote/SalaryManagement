const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
    }
    return process.env.NEXT_PUBLIC_API_URL || 'http://backend:5000';
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
};

const API_BASE_URL = getApiBaseUrl();

async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include',
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    throw error;
  }
}

export const api = {
  login: async (username, password) => {
    return fetchAPI('/api/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },

  signup: async (username, password, name) => {
    return fetchAPI('/api/signup', {
      method: 'POST',
      body: JSON.stringify({ username, password, name }),
    });
  },

  logout: async () => {
    return fetchAPI('/api/logout', {
      method: 'POST',
    });
  },

  getCurrentUser: async () => {
    return fetchAPI('/api/me');
  },
};

export default api;