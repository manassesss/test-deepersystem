<template>
  <div class="p-m-4 !w-full !flex">
    <h2>User Details</h2>
    <div v-if="user">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
      <p><strong>Timezone:</strong> {{ user.preferences.timezone }}</p>
      <p><strong>Is Active?</strong> {{ user.active ? 'Yes' : 'No' }}</p>
      <p><strong>Last Updated At:</strong> {{ formatDate(user.updated_ts) }}</p>
      <p><strong>Created At:</strong> {{ formatDate(user.created_ts) }}</p>

      <div class="p-mt-3">
        <Button label="Edit" icon="pi pi-pencil" @click="editUser" class="p-mr-2" />
        <Button label="Delete" icon="pi pi-trash" @click="confirmDelete" />
      </div>
    </div>

    <!-- Diálogo de confirmação para deleção -->
    <ConfirmDialog header="Confirm" icon="pi pi-exclamation-triangle" v-model:visible="showConfirmDialog" message="Are you sure you want to delete this user?" acceptLabel="Yes" rejectLabel="No" @accept="deleteUser" />

    <!-- Componente para editar usuário -->
    <UserForm v-if="showUserForm" :user="user" @close="closeUserForm" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Button from 'primevue/button';
import ConfirmDialog from 'primevue/confirmdialog';
import UserForm from './UsersForm.vue';
import { getUser, deleteUser as deleteUserApi } from '../api/userApi';

export default {
  name: 'UserDatail',
  components: {
    Button,
    ConfirmDialog,
    UserForm,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = ref(null);
    const showConfirmDialog = ref(false);
    const showUserForm = ref(false);

    const loadUser = async () => {
      try {
        // Obtém o _id do usuário dos parâmetros da rota
        user.value = await getUser(route.params.username);
      } catch (error) {
        console.error('Error loading user:', error);
      }
    };

    const formatDate = (timestamp) => {
      if (!timestamp) return '-';
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    };

    const confirmDelete = () => {
      showConfirmDialog.value = true;
    };

    const deleteUser = async () => {
      try {
        await deleteUserApi(user.value._id);
        router.push('/');
      } catch (error) {
        console.error('Error deleting user:', error);
      }
      showConfirmDialog.value = false;
    };

    const editUser = () => {
      showUserForm.value = true;
    };

    const closeUserForm = async () => {
      showUserForm.value = false;
      await loadUser();
    };

    onMounted(loadUser);

    return {
      user,
      formatDate,
      showConfirmDialog,
      confirmDelete,
      deleteUser,
      showUserForm,
      editUser,
      closeUserForm,
    };
  },
};
</script>

<style scoped>
.p-m-4 {
  margin: 1rem;
}
</style>
