import { DataTableColumns } from 'naive-ui';
import { h } from 'vue';

import ChatModelTagsRow from '@/components/ChatModelTagsRow.vue';
import ChatTypeTagInfoCell from '@/components/ChatTypeTagInfoCell.vue';
import { i18n } from '@/i18n';
import { apiChatModelNames, revChatModelNames } from '@/types/json_schema';
import { chatStatusMap, UserRead, UserSettingSchema } from '@/types/schema';
import { getCountTrans } from '@/utils/chat';

const t = i18n.global.t as any;

export const renderUserPerModelCounts = (setting: UserSettingSchema, availableOnly = false) => {
  const revCounts = {} as Record<string, string>;
  const apiCounts = {} as Record<string, string>;
  if (availableOnly) {
    setting.rev.available_models.forEach((model) => {
      revCounts[model] = getCountTrans(setting.rev.per_model_ask_count[model]);
    });
    setting.api.available_models.forEach((model) => {
      apiCounts[model] = getCountTrans(setting.api.per_model_ask_count[model]);
    });
  } else {
    revChatModelNames.forEach((model) => {
      revCounts[model] = getCountTrans(setting.rev.per_model_ask_count[model]);
    }
    );
    apiChatModelNames.forEach((model) => {
      apiCounts[model] = getCountTrans(setting.api.per_model_ask_count[model]);
    }
    );
  }
  // console.log(revCounts, apiCounts);
  return h(ChatTypeTagInfoCell, {
    value: {
      rev: h(ChatModelTagsRow, {
        value: revCounts,
      }),
      api: h(ChatModelTagsRow, {
        value: apiCounts,
      }),
    },
  });
};

type ListAttr<T> = {
  title: string;
  key: string;
  render?: (row: T) => any;
};

// 用于 UserProfile，复用了一部分 user_manager 代码
export function getUserAttrColumns(): ListAttr<UserRead>[] {
  return [
    { title: '#', key: 'id' },
    { title: t('commons.username'), key: 'username' },
    { title: t('commons.email'), key: 'email' },
    { title: t('commons.nickname'), key: 'nickname' },
    {
      title: t('labels.rev_chat_status'),
      key: 'rev_chat_status',
      render(row) {
        return row.rev_chat_status ? t(chatStatusMap[row.rev_chat_status as keyof typeof chatStatusMap]) : '';
      },
    },
    {
      title: t('labels.last_active_time'),
      key: 'last_active_time',
      render(row) {
        return row.last_active_time ? new Date(row.last_active_time).toLocaleString() : t('commons.neverActive');
      },
    },
    {
      title: `${t('labels.ask_count_limits')}`,
      key: 'ask_count_limits',
      render(row) {
        return h(ChatTypeTagInfoCell, {
          value: {
            rev: getCountTrans(row.setting.rev.max_conv_count),
            api: getCountTrans(row.setting.api.max_conv_count),
          },
        });
      },
    },
    {
      title: t('labels.available_ask_count'),
      key: 'available_ask_count',
      render(row) {
        // return getCountTrans(row.available_ask_count!);
        return renderUserPerModelCounts(row.setting, true);
      },
    },
  ];
}
