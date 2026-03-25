/**
 * API service for communicating with ChainGuard backend.
 */

import axios from "axios";

const API_BASE = "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

export const retrieveFile = async (fileName) => {
  const response = await api.get(`/file/${fileName}`, {
    responseType: "blob",
  });

  return {
    blob: response.data,
    headers: {
      status: response.headers["x-chainguard-status"],
      cid: response.headers["x-chainguard-cid"],
      verified: response.headers["x-chainguard-blockchain-verified"],
      registeredBy: response.headers["x-chainguard-registered-by"],
      timestamp: response.headers["x-chainguard-timestamp"],
    },
  };
};

export const verifyFile = async (fileName) => {
  const response = await api.get(`/verify/${fileName}`);
  return response.data;
};

export const listFiles = async () => {
  const response = await api.get("/registry");
  return response.data;
};

export const getFileHistory = async (fileName) => {
  const response = await api.get(`/registry/${fileName}/history`);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get("/health");
  return response.data;
};
