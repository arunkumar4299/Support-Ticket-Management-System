import axios from "axios";
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||"http://127.0.0.1:8000/api/v1"});
api.interceptors.request.use(config=>{const token=localStorage.getItem("accessToken"); if(token) config.headers.Authorization=`Bearer ${token}`; return config;});
export async function login(email:string,password:string){const r=await api.post("/auth/login",{email,password}); localStorage.setItem("accessToken",r.data.access_token); localStorage.setItem("refreshToken",r.data.refresh_token); return r.data;}
