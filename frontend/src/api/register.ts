import {UserCreate } from "@/types/schema";
import axios from "axios";
import ApiUrl from "./url";

export function registeruserApi(userInfo: UserCreate) {
  return axios.post<any>(ApiUrl.RegisterUser, userInfo);
}
