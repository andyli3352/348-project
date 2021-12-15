<template>
<div>

  <!-- Modal for displaying song report -->
  <b-modal ref="generateSongModal"
         id="generate-song-modal"
         title="Report for a song"
         hide-footer>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Happiness</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in songusers" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.happiness }}</td>
            </tr>
          </tbody>
        </table>
  </b-modal>

  <!-- modal for song report -->
  <b-modal ref="reportSongModal"
         id="report-song-modal"
         title="Report for a song"
         hide-footer>
  <b-form @submit="onReportSubmit" @reset="onReportReset" class="w-100">
  <b-form-group id="form-name-group"
                label="Song name:"
                label-for="form-name-input">
      <b-form-input id="form-name-input"
                    type="text"
                    v-model="reportSongForm.name"
                    required
                    placeholder="Enter song name">
      </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary" v-b-modal.generate-song-modal>Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
  </b-modal>

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
                    v-model="addSongForm.name"
                    required
                    placeholder="Enter song name">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-artist-group"
                  label="Artist:"
                  label-for="form-artist-input">
        <b-form-input id="form-artist-input"
                      type="text"
                      v-model="addSongForm.artist"
                      required
                      placeholder="Enter artist">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-length-group"
                  label="Length:"
                  label-for="form-length-input">
      <b-form-input id="form-length-input"
                      type="text"
                      v-model="addSongForm.length"
                      required
                      placeholder="Enter length">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-genre-group"
                  label="Genre:"
                  label-for="form-genre-input">
      <b-form-input id="form-genre-input"
                      type="text"
                      v-model="addSongForm.genre"
                      required
                      placeholder="Enter genre">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-happiness-group"
                  label="Happiness:"
                  label-for="form-happiness-input">
      <b-form-input id="form-happiness-input"
                      type="text"
                      v-model="addSongForm.happiness"
                      required
                      placeholder="Enter happiness">
        </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

<!-- modal for updating a song -->
  <b-modal ref="updateSongModal"
         id="update-song-modal"
         title="Update a song"
         hide-footer>
  <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
  <b-form-group id="form-name-update-group"
                label="Song name:"
                label-for="form-name-update-input">
      <b-form-input id="form-name-update-input"
                    type="text"
                    v-model="updateSongForm.name"
                    required
                    placeholder="Enter song name">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-artist-update-group"
                  label="Artist:"
                  label-for="form-artist-update-input">
        <b-form-input id="form-artist-update-input"
                      type="text"
                      v-model="updateSongForm.artist"
                      required
                      placeholder="Enter artist">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-length-update-group">
      <b-form-input id="form-length-update-input"
                      type="text"
                      v-model="updateSongForm.length"
                      required
                      placeholder="Enter length">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-genre-update-group">
      <b-form-input id="form-genre-update-input"
                      type="text"
                      v-model="updateSongForm.genre"
                      required
                      placeholder="Enter genre">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-happiness-update-group">
      <b-form-input id="form-happiness-update-input"
                      type="text"
                      v-model="updateSongForm.happiness"
                      required
                      placeholder="Enter happiness">
        </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

    <div class="row">
    <div class="col-sm-10">
     <button type="button" class="btn btn-success btn-sm" style="margin:5px;" v-b-modal.song-modal>
       Add Song</button>
     <button type="button" class="btn btn-success btn-sm" v-b-modal.report-song-modal>
       Song Report</button>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Song Name</th>
              <th scope="col">Artist</th>
              <th scope="col">Length</th>
              <th scope="col">Genre</th>
              <th scope="col">Number Assigned</th>
              <th scope="col">Happiness</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(song, index) in songs" :key="index">
              <td>{{ song.name }}</td>
              <td>{{ song.artist }}</td>
              <td>{{ song.length }}</td>
              <td>{{ song.genre }}</td>
              <td>{{ song.num_assigned }}</td>
              <td>{{ song.happiness }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.update-song-modal
                  >Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  v-on:click="deleteSong(index)">Delete</button>
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
  name: 'Songs',
  data() {
    return {
      songs: [],
      songusers: [],
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
      },
      reportSongForm: {
        name: '',
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
    addSong(payload) {
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
        name: this.songs[index].name,
        artist: this.songs[index].artist,
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
    reportSong(payload) {
      const path = 'http://localhost:5000/api/songuser';
      axios.post(path, payload)
        .then((res) => {
          this.songusers = res.data.songusers;
        })
        .catch((error) => {
          console.log(error);
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
    initReportForm() {
      this.reportSongForm.name = '';
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
    onReportSubmit(evt) {
      evt.preventDefault();
      this.$refs.reportSongModal.hide();
      const payload = {
        name: this.reportSongForm.name,
      };
      this.reportSong(payload);
      this.initReportForm();
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
    onReportReset(evt) {
      evt.preventDefault();
      this.$refs.reportSongModal.hide();
      this.initReportForm();
    },
  },
  created() {
    this.getSongs();
  },
};
</script>
