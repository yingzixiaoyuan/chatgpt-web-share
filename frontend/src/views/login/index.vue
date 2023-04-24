<template>
  <!-- Login Form -->
  <div class="flex justify-center items-center mt-20">
    <n-form ref="formRef" :model="formValue" :rules="loginRules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
      <n-form-item :label="$t('commons.username')" path="username">
        <n-input v-model:value="formValue.username" :placeholder="$t('tips.pleaseEnterUsername')" :input-props="{
          autoComplete: 'username'
        }" />
      </n-form-item>
      <n-form-item :label="$t('commons.password')" path="password">
        <n-input type="password" show-password-on="click" v-model:value="formValue.password" :placeholder="$t('tips.pleaseEnterPassword')" :input-props="{
          autoComplete: 'current-password'
        }" @keyup.enter="login" />
      </n-form-item>
      <n-form-item wrapper-col="{ span: 16, offset: 8 }">
        <n-button type="primary" @click="login" :enabled="loading">{{ $t("commons.login") }}</n-button>
        <n-button type="primary" @click="register" style="margin-left:10px">{{ $t("commons.register") }}</n-button>
      </n-form-item>
    </n-form>
  </div>

  <div id="content">
  &nbsp;&nbsp;Aichat火爆ing🔥🔥, 共享key大家免费使用。<br>
  &nbsp;&nbsp;为防止部分同学恶意刷问题浪费资源，提供了邮箱注册登录功能。<br>
  &nbsp;&nbsp;不注册:可通过test:test账户进行试用,每天限额1000次,人多可能很快用完。<br>
  &nbsp;&nbsp;✋🏻注册步骤: 点击注册 --> 提供邮箱 --> 邮件内链接激活账号.<br>
  &nbsp;&nbsp;声明:⭐️本站不保存任何聊天信息，页面刷新即丢失，需复用请及时保存。<br>
  &nbsp;&nbsp;网站无法访问请联系ikeyitop@163.com<br>
  &nbsp;&nbsp;如果喜欢，请打赏我一瓶矿泉书、🍗~ <br>
  </div>
  <div style="text-align: center;">
  <img src="/QRcode.jpg" width="200" height="150" style="max-width: 100%; max-height: 100%;">
</div>

</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useUserStore } from '@/store';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { loginApi, LoginData } from '@/api/user';
import { Message } from '@/utils/tips';
import { FormValidationError } from 'naive-ui/es/form';
import { FormInst } from 'naive-ui'

const router = useRouter();
const { t } = useI18n();
const userStore = useUserStore();
const formRef = ref<FormInst>();

const formValue = reactive({
  username: '',
  password: ''
});
const loading = ref(false);
const loginRules = {
  username: { required: true, message: t("tips.pleaseEnterUsername"), trigger: 'blur' },
  password: { required: true, message: t("tips.pleaseEnterPassword"), trigger: 'blur' }
}
const register = () => {
  router.push({ name: 'register' });
}
const login = async () => {
  if (loading.value) return;
  formRef.value?.validate((errors?: Array<FormValidationError>) => {
    if (!errors) {
      loading.value = true;
    }
  }).then(async () => {
    try {
        await userStore.login(formValue as LoginData);
        const { redirect, ...othersQuery } = router.currentRoute.value.query;
        await userStore.fetchUserInfo();
        Message.success(t('tips.loginSuccess'));
        await router.push({
          name: userStore.user?.is_superuser ? 'admin' : 'conversation'
        });
        // TODO: 记住密码
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