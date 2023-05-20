import { createPinia } from 'pinia';

import useAppStore from './modules/app';
import useRegisterStore from "./modules/register";
import useConversationStore from './modules/conversation';
import useUserStore from './modules/user';

const pinia = createPinia();

export { useAppStore, useConversationStore, useUserStore,useRegisterStore };

export default pinia;
