<template>
<div>

  <!-- modal for adding a song -->
  <b-modal ref="addSongModal"
         id="song-modal"
         title="Add a new song"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-name-group"
                label="Song name:"
                label-for="form-name-input">
      <b-form-input id="form-name-input"
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
     <button type="button" class="btn btn-success btn-sm" v-b-modal.song-modal>Add Song</button>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Song Name</th>
              <th scope="col">Artist</th>
              <th scope="col">Length</th>
              <th scope="col">Genre</th>
              <th scope="col"></th>
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
      songs: [],
      addSongForm: {
        name: '',
        artist: '',
        length: 0,
        genre: '',
        happiness: 0,
      },
      updateSongForm: {
        name: '',
        artist: '',
        length: 0,
        genre: '',
        happiness: 0,
        num_assigned: 0,
      },
    };
  },
  methods: {
    getSongs() {
      const path = 'http://localhost:5000/api/songs';
      axios.get(path)
        .then((res) => {
          console.log(res.data.songs);
          this.songs = res.data.songs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser(payload) {
      const path = 'http://localhost:5000/api/songs/add';
      axios.post(path, payload)
        .then(() => {
          this.getSongs();
        })
        .catch((error) => {
          console.error(error);
          this.getSongs();
        });
    },
    deleteSong(index) {
      const payload = {
        username: this.users[index].username,
      };
      const path = 'http://localhost:5000/api/songs/delete';
      axios.post(path, payload)
        .then(() => {
          this.getSongs();
        })
        .catch((error) => {
          console.error(error);
          this.getSongs();
        });
    },
    updateSong(payload) {
      const path = 'http://localhost:5000/api/songs/update';
      axios.post(path, payload)
        .then(() => {
          this.getSongs();
        })
        .catch((error) => {
          console.error(error);
          this.getSongs();
        });
    },
    initForm() {
      this.addSongForm.name = '';
      this.addSongForm.artist = '';
      this.addSongForm.length = 0;
      this.addSongForm.genre = '';
      this.addSongForm.happiness = 0;
    },
    initUpdateForm() {
      this.updateSongForm.name = '';
      this.updateSongForm.artist = '';
      this.updateSongForm.length = 0;
      this.updateSongForm.genre = '';
      this.updateSongForm.num_assigned = 0;
      this.updateSongForm.happiness = 0;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      const payload = {
        name: this.addSongForm.name,
        artist: this.addSongForm.artist,
        length: this.addSongForm.length,
        genre: this.addSongForm.genre,
        happiness: this.addSongForm.happiness,
      };
      this.addSong(payload);
      this.initForm();
    },
    onUpdateSubmit(evt) {
      evt.preventDefault();
      this.$refs.updateSongModal.hide();
      const payload = {
        name: this.updateSongForm.name,
        artist: this.updateSongForm.artist,
        length: this.updateSongForm.length,
        genre: this.updateSongForm.genre,
        num_assigned: this.updateSongForm.num_assigned,
        happiness: this.updateSongForm.happiness,
      };
      this.updateSong(payload);
      this.initUpdateForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addSongModal.hide();
      this.initForm();
    },
    onUpdateReset(evt) {
      evt.preventDefault();
      this.$refs.updateSongModal.hide();
      this.initUpdateForm();
    },
  },
  created() {
    this.getSongs();
  },
};
</script>
