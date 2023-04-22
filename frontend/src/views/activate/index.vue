<template>
  <div></div>
</template>

<script lang="ts" setup>
  import {useRoute } from 'vue-router';
  import { useUserStore } from '@/store';
  import { Message } from '@/utils/tips';
  import { useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import { ref } from 'vue';

  // const router = useRouter();
  const route = useRoute();
  const userStore = useUserStore();
  const token = route.params.token as string;
  console.log("get token",token)
  const router = useRouter();
  const { t } = useI18n();
  const loading = ref(false);

  const activate = async () => {
    try {
      await userStore.activate(token);
      Message.success(t('tips.activateSuccess')+'3秒之后跳转到登录页面');
          setTimeout(function(){
            router.push({ name: 'login' });
          },3000);
      // await router.push({
      //   name: 'login'
      // });
    } catch (error) {
      console.log(error);
    } finally {
      loading.value = false;
    }
  }
  activate()
  // router.replace({ path: gotoPath });
</script>

<style scoped lang="less"></style>
