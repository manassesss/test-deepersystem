<template>
  <Dialog header="User Form" v-model:visible="visible" modal>
    <div class="p-fluid">
      <div class="p-field">
        <label for="username">Username</label>
        <InputText id="username" v-model="form.username" />
      </div>
      <div class="p-field" v-if="!isEdit">
        <label for="password">Password</label>
        <Password id="password" v-model="form.password" feedback="false" />
      </div>
      <div class="p-field">
        <label for="roles">Roles</label>
        <MultiSelect id="roles" v-model="form.roles" :options="rolesOptions" optionLabel="name" optionValue="name" />
      </div>
      <div class="p-field">
        <label for="timezone">Timezone</label>
        <InputText id="timezone" v-model="form.preferences.timezone" />
      </div>
      <div class="p-field-checkbox">
        <Checkbox v-model="form.active" inputId="active" />
        <label for="active">Active</label>
      </div>
    </div>
    <template #footer>
      <Button label="Cancel" @click="close" class="p-button-text" />
      <Button label="Save" @click="saveUser" />
    </template>
  </Dialog>
</template>

<script>
import { ref, watch, computed } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import MultiSelect from 'primevue/multiselect';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';
import { createUser, updateUser } from '../api/userApi';

export default {
  name: 'UserForm',
  components: { Dialog, InputText, Password, MultiSelect, Checkbox, Button },
  props: {
    user: {
      type: Object,
      default: null,
    },
  },
  emits: ['close'],
  setup(props, { emit }) {
    const visible = ref(true);
    const rolesOptions = ref([{ name: 'admin' }, { name: 'manager' }, { name: 'tester' }]);
    const form = ref({
      username: '',
      password: '',
      roles: [],
      preferences: {
        timezone: '',
      },
      active: true,
    });

    // Determina se estamos editando (true) ou criando (false)
    const isEdit = computed(() => !!props.user);

    watch(
      () => props.user,
      (newUser) => {
        if (newUser) {
          form.value = { ...newUser };
        } else {
          form.value = {
            username: '',
            password: '',
            roles: [],
            preferences: { timezone: '' },
            active: true,
          };
        }
      },
      { immediate: true }
    );

    const close = () => {
      visible.value = false;
      emit('close');
    };

    const saveUser = async () => {
      try {
        if (isEdit.value) {
          await updateUser(form.value._id, form.value);
        } else {
          await createUser(form.value);
        }
        close();
      } catch (error) {
        console.error('Error saving user:', error);
      }
    };

    return {
      visible,
      form,
      rolesOptions,
      close,
      saveUser,
      isEdit,
    };
  },
};
</script>
