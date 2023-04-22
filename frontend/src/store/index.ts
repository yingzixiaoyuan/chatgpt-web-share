import { createPinia } from "pinia";
import useAppStore from "./modules/app";
import useUserStore from "./modules/user";
import useRegisterStore from "./modules/register";
import useConversationStore from "./modules/conversation";

const pinia = createPinia();

export { useAppStore, useUserStore, useConversationStore,useRegisterStore };
export default pinia;
