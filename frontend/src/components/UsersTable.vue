<template>
  <div class="p-m-4 p-4 w-full">
    <div class="header-title">
      <h1 class="text-2xl font-semibold">Users List</h1>
      <Button label="Create User" icon="pi pi-plus" @click="openCreateDialog" />
    </div>
    
    <div class="mt-4 content">
      <ProgressSpinner v-if="loading" />
      <DataTable v-else :value="users" responsiveLayout="scroll">
        <Column field="username" header="Username">
          <template #body="slotProps">
            <router-link :to="`/user/${slotProps.data.username}`">
              {{ slotProps.data.username }}
            </router-link>
          </template>
        </Column>
        <Column field="roles" header="Roles">
          <template #body="slotProps">
            {{ slotProps.data.roles.join(', ') }}
          </template>
        </Column>
        <Column field="preferences.timezone" header="Timezone">
          <template #body="slotProps">
            {{ slotProps.data.preferences.timezone }}
          </template>
        </Column>
        <Column field="active" header="Is Active?">
          <template #body="slotProps">
            {{ slotProps.data.active ? 'Yes' : 'No' }}
          </template>
        </Column>
        <Column field="updated_ts" header="Last Updated At">
          <template #body="slotProps">
            {{ formatDate(slotProps.data.updated_ts) }}
          </template>
        </Column>
        <Column field="created_ts" header="Created At">
          <template #body="slotProps">
            {{ formatDate(slotProps.data.created_ts) }}
          </template>
        </Column>
        <Column header="Actions">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" severity="secondary" class="mr-2" @click="editUser(slotProps.data)" />
            <Button icon="pi pi-trash" severity="danger" @click="confirmDelete(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Modal de Confirmação para Deletar Usuário -->
    <ConfirmDialog 
      header="Confirm Deletion"
      icon="pi pi-exclamation-triangle"
      :v-model:visible="showConfirmDialog"
      :message="`Are you sure you want to delete user '${userToDelete?.username}'?`"
      acceptLabel="Yes"
      rejectLabel="No"
      @accept="deleteUser"
    />

    <!-- Formulário de Usuário -->
    <UserForm v-if="showUserForm" :user="selectedUser" @close="closeUserForm" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import ConfirmDialog from 'primevue/confirmdialog';
import ProgressSpinner from 'primevue/progressspinner';
import UserForm from './UsersForm.vue';
import { getUsers, deleteUser as deleteUserApi } from '../api/userApi';

export default {
  name: 'UsersTable',
  components: {
    DataTable,
    Column,
    Button,
    ConfirmDialog,
    ProgressSpinner,
    UserForm,
  },
  setup() {
    const users = ref([]);
    const showConfirmDialog = ref(false);
    const showUserForm = ref(false);
    const selectedUser = ref(null);
    const userToDelete = ref(null);
    const loading = ref(true);

    const loadUsers = async () => {
      loading.value = true;
      try {
        users.value = await getUsers();
      } catch (error) {
        console.error('Error loading users:', error);
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (timestamp) => {
      if (!timestamp) return '-';
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    };

    const confirmDelete = (user) => {
      if (!user) return;
      userToDelete.value = user;
      showConfirmDialog.value = true;
    };

    const deleteUser = async () => {
      if (!userToDelete.value) return;

      try {
        loading.value = true;
        await deleteUserApi(userToDelete.value._id);
        await loadUsers(); // Atualiza a lista após exclusão
      } catch (error) {
        console.error('Error deleting user:', error);
      } finally {
        loading.value = false;
        showConfirmDialog.value = false;
        userToDelete.value = null;
      }
    };

    const editUser = (user) => {
      selectedUser.value = { ...user };
      showUserForm.value = true;
    };

    const openCreateDialog = () => {
      selectedUser.value = null;
      showUserForm.value = true;
    };

    const closeUserForm = async () => {
      showUserForm.value = false;
      selectedUser.value = null;
      await loadUsers();
    };

    onMounted(loadUsers);

    return {
      users,
      formatDate,
      showConfirmDialog,
      confirmDelete,
      deleteUser,
      showUserForm,
      openCreateDialog,
      editUser,
      selectedUser,
      closeUserForm,
      loading,
      userToDelete,
    };
  },
};
</script>

<style scoped>
.p-m-4 {
  margin: 1rem;
}
.mr-2 {
  margin-right: 0.5rem;
}
.mt-4 {
  margin-top: 1rem;
}
.header-title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
.content {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
