
import {registeruserApi,activateuserApi} from "@/api/register";
import { defineStore } from "pinia";
import { UserCreate,UserRead } from "@/types/schema";
import { RegisterUserState } from "../types";

const useRegisterStore = defineStore("register", {
  state: (): RegisterUserState => ({
    user: null
  }),
  getters: {
    userInfo(state: RegisterUserState): UserRead | null {
      return state.user;
    },
  },
  actions: {
    setInfo(user: UserRead) {
      this.$patch({ user });
    },
    // Register
    async register(userInfo: UserCreate) {
      try {
        const user = (await registeruserApi(userInfo)).data;
        this.setInfo(user);
      } catch (err) {
        throw err
      }
    }
  },
});

export default useRegisterStore;
