import axios, { AxiosRequestConfig } from "axios";

// backend server url
export const BASE_URL =
  process.env.NEXT_PUBLIC_SERVER_URL || "http://107.21.53.156";

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
      let errorMessages = "";
      keys.forEach((item) => {
        if (item === "image") {
          const newObj = err.response.data[item];
          Object.keys(newObj).forEach((itm) => {
            errorMessages += `${itm.toUpperCase()}: ${newObj[itm]} \n`;
          });
        } else {
          errorMessages += `${item.toUpperCase()}: ${
            err.response.data[item]
          } \n`;
        }
      });
      return errorMessages.trim();
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

const getParkingSpot = async () => {
  const api = `${BASE_URL}/api/parking-list/`;

  try {
    const response = await getData(api);
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

const getSingleParkingSpot = async (id: string) => {
  const api = `${BASE_URL}/api/parking-status/${id}/`;

  try {
    const response = await getData(api);
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

const confirmParkingSpot = async (repo: any) => {
  const api = `${BASE_URL}/api/bookings/`;

  const token = localStorage.getItem("token");

  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };

  try {
    const response = await postData(api, repo, config);
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

const getMyBookings = async () => {
  const api = `${BASE_URL}/api/bookings/`;

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

export {
  login,
  register,
  updateUser,
  setJwtToken,
  getJwtToken,
  getUser,
  getParkingSpot,
  getSingleParkingSpot,
  confirmParkingSpot,
  getMyBookings,
};
