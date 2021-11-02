<template>
<div>

  <!-- modal for updating a user -->
  <b-modal ref="addUserModal"
         id="user-modal"
         title="Add a new user"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-username-group"
                label="Username:"
                label-for="form-username-input">
      <b-form-input id="form-username-input"
                    type="text"
                    v-model="addUserForm.username"
                    required
                    placeholder="Enter username">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-password-group"
                  label="Password:"
                  label-for="form-password-input">
        <b-form-input id="form-password-input"
                      type="text"
                      v-model="addUserForm.password"
                      required
                      placeholder="Enter password">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-happiness-group">
      <b-form-input id="form-happiness-input"
                      type="text"
                      v-model="addUserForm.happiness"
                      required
                      placeholder="Enter happiness">
        </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

<!-- modal for updating a user -->
  <b-modal ref="updateUserModal"
         id="update-user-modal"
         title="Update an user"
         hide-footer>
  <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
  <b-form-group id="form-username-update-group"
                label="Username:"
                label-for="form-username-update-input">
      <b-form-input id="form-username-update-input"
                    type="text"
                    v-model="updateUserForm.username"
                    required
                    placeholder="Enter username">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-password-update-group"
                  label="Password:"
                  label-for="form-password-update-input">
        <b-form-input id="form-password-update-input"
                      type="text"
                      v-model="updateUserForm.password"
                      required
                      placeholder="Enter password">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-happiness-update-group">
      <b-form-input id="form-happiness-update-input"
                      type="text"
                      v-model="updateUserForm.happiness"
                      required
                      placeholder="Enter happiness">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-age-update-group">
      <b-form-input id="form-age-update-input"
                      type="text"
                      v-model="updateUserForm.age"
                      required
                      placeholder="Enter account age">
        </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

    <div class="row">
    <div class="col-sm-10">
      <h>Users Table</h>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Password</th>
              <th scope="col">Happiness</th>
              <th scope="col">Average Happiness</th>
              <th scope="col">Global Happiness Average</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.password }}</td>
              <td>{{ user.happiness }}</td>
              <td>{{ user.average_happiness }}</td>
              <td>{{ user.total_avg }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.update-user-modal
                  >Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  v-on:click="deleteUser(index)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

     <button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal>Add User</button>
    </div>
    </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      addUserForm: {
        username: '',
        password: '',
        happiness: 0,
      },
      updateUserForm: {
        username: '',
        password: '',
        happiness: 0,
        age: 0,
      },
    };
  },
  methods: {
    getUsers() {
      const path = 'http://localhost:5000/api/users';
      axios.get(path)
        .then((res) => {
          console.log(res.data.users);
          this.users = res.data.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser(payload) {
      const path = 'http://localhost:5000/api/users/add';
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
          this.getUsers();
        });
    },
    deleteUser(index) {
      const payload = {
        username: this.users[index].username,
      };
      const path = 'http://localhost:5000/api/users/delete';
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
          this.getUsers();
        });
    },
    updateUser(payload) {
      const path = 'http://localhost:5000/api/users/update';
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
          this.getUsers();
        });
    },
    initForm() {
      this.addUserForm.username = '';
      this.addUserForm.password = '';
      this.addUserForm.happiness = 0;
    },
    initUpdateForm() {
      this.updateUserForm.username = '';
      this.updateUserForm.password = '';
      this.updateUserForm.happiness = 0;
      this.updateUserForm.age = 0;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      const payload = {
        username: this.addUserForm.username,
        password: this.addUserForm.password,
        happiness: this.addUserForm.happiness,
      };
      this.addUser(payload);
      this.initForm();
    },
    onUpdateSubmit(evt) {
      evt.preventDefault();
      this.$refs.updateUserModal.hide();
      const payload = {
        username: this.updateUserForm.username,
        password: this.updateUserForm.password,
        happiness: this.updateUserForm.happiness,
      };
      this.updateUser(payload);
      this.initUpdateForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
    onUpdateReset(evt) {
      evt.preventDefault();
      this.$refs.updateUserModal.hide();
      this.initUpdateForm();
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
