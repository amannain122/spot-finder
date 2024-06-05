import axios, { AxiosRequestConfig } from "axios";

export const BASE_URL = "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 50000,
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return Promise.resolve(response);
  },
  (error) => {
    return Promise.reject(error);
  }
);

const getData = async (
  url: string,
  config?: AxiosRequestConfig<any> | undefined
) => axiosInstance.get(url, config);

const postData = async (
  url: string,
  data: any,
  config?: AxiosRequestConfig<any> | undefined
) => axiosInstance.post(url, data, config);

const patchData = async (
  url: string,
  data: any,
  config?: AxiosRequestConfig<any> | undefined
) => axiosInstance.patch(url, data, config);

const putData = async (
  url: string,
  data: any,
  config?: AxiosRequestConfig<any> | undefined
) => axiosInstance.put(url, data, config);

const deleteData = async (
  url: string,
  config?: AxiosRequestConfig<any> | undefined
) => axiosInstance.delete(url, config);

const getJwtToken = () => {
  return localStorage?.getItem("token");
};

const setJwtToken = (token: string) => {
  localStorage?.setItem("token", token);
};

const login = async (repo: any) => {
  const api = `${BASE_URL}/api/login/`;
  try {
    const response = await postData(api, repo);
    if (response.data) {
      localStorage?.setItem("token", response.data.token);
    }
    return {
      status: "success",
      data: response.data,
    };
  } catch (error) {
    return {
      status: "failure",
      data: error,
    };
  }
};

const register = async (repo: any) => {
  const api = `${BASE_URL}/api/user/`;
  try {
    const response = await postData(api, repo);
    return {
      status: "success",
      data: response.data,
    };
  } catch (error) {
    return {
      status: "failure",
      data: error,
    };
  }
};

const updateUser = async (repo: any) => {
  const api = `${BASE_URL}/api/user/`;
  const token = localStorage.getItem("token");

  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };

  try {
    const response = await patchData(api, repo, config);
    return {
      status: "success",
      data: response.data,
    };
  } catch (error) {
    return {
      status: "failure",
      data: error,
    };
  }
};

const getUser = async () => {
  const api = `${BASE_URL}/api/user/`;

  const token = localStorage.getItem("token");
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  try {
    const response = await getData(api, config);
    return {
      status: "success",
      data: response.data,
    };
  } catch (error) {
    return {
      status: "failure",
      data: error,
    };
  }
};

export const handleError = (err: any, showToast = true) => {
  if (err?.response) {
    if (err.response.data && typeof err.response.data === "object") {
      if (err.response.data.detail) {
        return err?.response?.data?.detail || "";
      }
      const keys = Object.keys(err.response.data);
      keys.forEach((item) => {
        if (item === "detail") {
          const newObj = err.response.data[item];
          if (typeof err.response.data[item] === "object") {
            Object.keys(newObj).forEach((itm) => {
              return newObj[itm];
            });
          } else {
            return err.response.data[item];
          }
        }
      });
    } else {
      return `Error with Status code : ${err.response.status}`;
    }
  } else if (err?.request) {
    if (err.request?.status < 100) {
      if (showToast) return "Network Error!";
    }
  } else {
    return err;
  }
};

export { login, register, updateUser, setJwtToken, getJwtToken, getUser };
