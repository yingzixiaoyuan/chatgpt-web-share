import {
  NDropdown,
  NButton,
  NIcon,
  NInput,
  NSelect,
  SelectOption,
} from "naive-ui";
import { h } from "vue";
import { MdMore } from "@vicons/ionicons4";
import { i18n } from "@/i18n";
import { ConversationSchema, ChatModels } from "@/types/schema";
import { Dialog } from "@/utils/tips";
import useUserStore from "@/store/modules/user";
import { ChatConversationDetail } from "@/types/custom";

const t = i18n.global.t as any;

const modelNameMap = {
  "text-davinci-002-render-sha": t("commons.shaModel"),
  "text-davinci-002-render-paid": t("commons.paidModel"),
  "gpt-4": t("commons.gpt4Model"),
};

const getModelNameTrans = (model_name: keyof typeof modelNameMap) => {
  return modelNameMap[model_name] || model_name;
};

const getCountTrans = (count: number): string => {
  return count == -1 ? t("commons.unlimited") : `${count}`;
};

const dropdownRenderer = (
  conversation: ConversationSchema,
  handleDeleteConversation: (conversation_id?: string) => void,
  handleChangeConversationTitle: (conversation_id?: string) => void
) =>
  h(
    NDropdown,
    {
      trigger: "hover",
      options: [
        {
          label: t("commons.delete"),
          key: "delete",
          props: {
            onClick: () =>
              handleDeleteConversation(conversation.conversation_id),
          },
        },
        {
          label: t("commons.rename"),
          key: "rename",
          props: {
            onClick: () =>
              handleChangeConversationTitle(conversation.conversation_id),
          },
        },
      ],
    },
    {
      default: () =>
        h(
          NButton,
          {
            size: "small",
            quaternary: true,
            circle: true,
          },
          { default: () => h(NIcon, null, { default: () => h(MdMore) }) }
        ),
    }
  );

const popupInputDialog = (
  title: string,
  placeholder: string,
  callback: (inp: string) => Promise<any>,
  success: () => void,
  fail: () => void
) => {
  let input = "";
  let secondInput: string | undefined = undefined;
  const d = Dialog.info({
    title: title,
    positiveText: t("commons.confirm"),
    negativeText: t("commons.cancel"),
    content: () =>
      h(NInput, {
        onInput: (e) => (input = e),
        autofocus: true,
        placeholder: placeholder,
      }),
    onPositiveClick() {
      d.loading = true;
      return new Promise((resolve) => {
        callback(input)
          .then(() => {
            success();
            resolve(true);
          })
          .catch(() => {
            fail();
            resolve(true);
          })
          .finally(() => {
            d.loading = false;
          });
      });
    },
  });
};

const getAvailableModelOptions = (): SelectOption[] => {
  const userStore = useUserStore();
  let options = [
    { label: t("commons.shaModel"), value: "gpt-3.5-turbo-0301" },
  ];
  if (userStore.user?.can_use_paid)
    options.push({
      label: t("commons.paidModel"),
      value: "text-davinci-002-render-paid",
    });
  if (userStore.user?.can_use_gpt4)
    options.push({ label: t("commons.gpt4Model"), value: "gpt-4" });
  return options;
};

const popupNewConversationDialog = (
  callback: (_conv_title: string, _conv_model: string) => Promise<any>
) => {
  let convTitle = "";
  let convModel = "";
  const d = Dialog.info({
    title: t("commons.newConversation"),
    positiveText: t("commons.confirm"),
    negativeText: t("commons.cancel"),
    // content: () =>
    //   h(NInput, { onInput: (e) => (input = e), autofocus: true, placeholder: placeholder, }),

    // 用一个 NInput 和一个 NSelect
    content: () =>
      h(
        "div",
        {
          style: "display: flex; flex-direction: column; gap: 16px;",
        },
        [
          h(NInput, {
            onInput: (e) => (convTitle = e),
            autofocus: true,
            placeholder: t("tips.conversationTitle"),
          }),
          h(NSelect, {
            placeholder: t("tips.whetherUsePaidModel"),
            "onUpdate:value": (value: string) => (convModel = value),
            options: getAvailableModelOptions(),
          }),
        ]
      ),
    onPositiveClick() {
      d.loading = true;
      return new Promise((resolve) => {
        callback(convTitle, convModel)
          .then(() => {
            resolve(true);
          })
          .catch(() => {
            resolve(true);
          })
          .finally(() => {
            d.loading = false;
          });
      });
    },
  });
};

const popupChangeConversationTitleDialog = (
  conversation_id: string,
  callback: (title: string) => Promise<any>,
  success: () => void,
  fail: () => void
) => {
  popupInputDialog(
    t("commons.rename"),
    t("tips.rename"),
    callback,
    success,
    fail
  );
};

const popupResetUserPasswordDialog = (
  callback: (password: string) => Promise<any>,
  success: () => void,
  fail: () => void
) => {
  popupInputDialog(
    t("commons.resetPassword"),
    t("tips.resetPassword"),
    callback,
    success,
    fail
  );
};

export {
  dropdownRenderer,
  popupNewConversationDialog,
  popupChangeConversationTitleDialog,
  popupResetUserPasswordDialog,
  getModelNameTrans,
  getCountTrans,
  modelNameMap
};
