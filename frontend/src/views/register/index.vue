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
      <n-form-item wrapper-col="{ span: 16, offset: 8 }">
        <n-button type="primary" @click="register" :enabled="loading" style="margin-left:10px">{{ $t("commons.register") }}</n-button>
      </n-form-item>
    </n-form>
    <n-modal 
      :show="showModal"
      style="width: 600px"
      preset="dialog"
      title="确认"
      size="huge"
      :bordered="false">
      {{t('tips.activeUser')}} {{ timeout / 1000 }} 秒之后跳转到登录页面
  </n-modal>
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

const router = useRouter();

const timeoutRef = ref(5000)
const showModalRef = ref(false)
const countdown = () => {
  if (timeoutRef.value <= 0) {
    showModalRef.value = false
    router.push({ name: 'login' });
  } else {
    timeoutRef.value -= 1000
    setTimeout(countdown, 1000)
  }
}

const showModal=showModalRef
const timeout= timeoutRef

const userStore = useUserStore();
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

function validatePassword(rule: FormItemRule, valPwd: string): boolean {
  if (valPwd.length < 6) {
      return false
    } 
  let arrVerify = [
    {regName: 'Number', regValue: /^.*[0-9]+.*/},
    {regName: 'LowerCase', regValue: /^.*[a-z]+.*/},
    {regName: 'UpperCase', regValue: /^.*[A-Z]+.*/},
    {regName: 'SpecialCharacters', regValue: /^.*[^a-zA-Z0-9]+.*/}
  ];
  let regNum = 0;// 记录匹配的次数
  for (let iReg = 0; iReg < arrVerify.length; iReg++) {
    if (arrVerify[iReg].regValue.test(valPwd)) {
      regNum = regNum + 1;
    }
  }
  return regNum >= 2
}

const loginRules = {
  username: { required: true, message: t("tips.pleaseEnterUsername"), trigger: 'blur' },
  password: { required: true, message: t("tips.pleaseEnterPassword"), trigger: ['input', 'blur'],validator: validatePassword },
  nickname: { required: true, trigger: 'blur',message: t("tips.pleaseEnterNickname") },
  email: { required: true, type: 'email', message: t("tips.pleaseEnterEmail") ,trigger: 'blur' },
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
          showModalRef.value = true
          timeoutRef.value = 6000
          countdown()
        }
      } catch (error) {
        console.log(error);
      } finally {
        loading.value = false;
      }
  });
}
  if (userStore.user) {
  router.push({ name: 'conversation' });
}
</script>

<style lang="scss" scoped>

</style>