<template>
<div class="flex justify-center items-center mt-20">
    <n-form ref="formRef" :model="formValue" :rules="loginRules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
      <n-form-item :label="$t('commons.username')" path="username">
        <n-input v-model:value="formValue.username" :placeholder="$t('tips.pleaseEnterUsername')" :input-props="{
          autoComplete: 'username'
        }" />
      </n-form-item>
      <n-form-item :label="$t('commons.nickname')" path="nickname">
        <n-input v-model:value="formValue.nickname" :placeholder="$t('tips.pleaseEnterNickname')" :input-props="{
          autoComplete: 'nickname'
        }" />
      </n-form-item>
      <n-form-item :label="$t('commons.email')" path="email">
        <n-input v-model:value="formValue.email" :placeholder="$t('tips.pleaseEnterEmail')" :input-props="{
          autoComplete: 'email'
        }" />
      </n-form-item>

      <n-form-item :label="$t('commons.password')" path="password">
        <n-input type="password" show-password-on="click" v-model:value="formValue.password" :placeholder="$t('tips.pleaseEnterPassword')" :input-props="{
          autoComplete: 'current-password'
        }" />
      </n-form-item>
      <n-form-item
      ref="rPasswordFormItemRef"
      first
      path="reenteredPassword"
      label="重复密码"
    >
      <n-input
        v-model:value="formValue.reenteredPassword"
        :placeholder="$t('tips.pleaseEnterPassword')"
        :disabled="!formValue.password"
        type="password"
        @keydown.enter.prevent
      />
    </n-form-item>


      <!-- <n-form-item :label="$t('commons.repeatedpassword')" path="repeatedpassword">
        <n-input type="password" show-password-on="click" v-model:value="formValue.repeatedpassword" :placeholder="$t('tips.pleaseEnterPassword')" :input-props="{
          autoComplete: 'current-password'
        }" />

      </n-form-item> -->
      <n-form-item wrapper-col="{ span: 16, offset: 8 }">
        <n-button type="primary" @click="register" :enabled="loading" style="margin-left:10px">{{ $t("commons.register") }}</n-button>
      </n-form-item>
    </n-form>
  </div>
</template>

<script setup lang="ts">
import { useRegisterStore } from '@/store';
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n';
import { FormInst,FormItemRule } from 'naive-ui'
import { FormValidationError } from 'naive-ui/es/form';
import {  UserCreate} from "@/types/schema";
import { Message } from '@/utils/tips';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store';

const userStore = useUserStore();

const router = useRouter();

const RegisterStore = useRegisterStore();
const formRef = ref<FormInst>();

const { t } = useI18n();
const formValue = reactive({
  username: null, 
  nickname: null,
  email: null,
  password: '',
  reenteredPassword: ''
});
const loading = ref(false);
function validatePasswordStartWith (
      rule: FormItemRule,
      value: string
    ): boolean {
      return (
        !!formValue.password &&
        formValue.password.startsWith(value) &&
        formValue.password.length >= value.length
      )
    }
function validatePasswordSame (rule: FormItemRule, value: string): boolean {
  return value === formValue.password
}

const loginRules = {
  username: { required: true, message: t("tips.pleaseEnterUsername"), trigger: 'blur' },
  password: { required: true, message: t("tips.pleaseEnterPassword"), trigger: 'blur' },
  nickname: { required: true, trigger: 'blur' },
  email: { required: true, type: 'email', message: 'Please enter a valid email address',trigger: 'blur' },
  reenteredPassword: [
        {
          required: true,
          message: '请再次输入密码',
          trigger: ['input', 'blur']
        },
        {
          validator: validatePasswordStartWith,
          message: '两次密码输入不一致',
          trigger: 'input'
        },
        {
          validator: validatePasswordSame,
          message: '两次密码输入不一致',
          trigger: ['blur', 'password-input']
        },
        
      ]
}

const register = async () => {
  if (loading.value) return;
  formRef.value?.validate((errors?: Array<FormValidationError>) => {
    if (!errors) {
      loading.value = true;
    }
  }).then(async () => {
    try { 
        await RegisterStore.register(formValue as unknown as  UserCreate);
        if (RegisterStore.userInfo){
          Message.success(t('tips.activeUser')+'3秒之后跳转到登录页面');
          setTimeout(function(){
            router.push({ name: 'login' });
          },3000);
        }
      } catch (error) {
        console.log(error);
      } finally {
        loading.value = false;
      }
  });
}
console.log("get console",userStore.user)
  if (userStore.user) {
  router.push({ name: 'conversation' });
}
</script>

<style lang="scss" scoped>

</style>