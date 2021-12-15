<template>
<div>

  <!-- Modal for displaying quote report -->
  <b-modal ref="generateQuoteModal"
         id="generate-quote-modal"
         title="Report for a quote"
         hide-footer>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Happiness</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in quoteusers" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.happiness }}</td>
            </tr>
          </tbody>
        </table>
  </b-modal>

  <!-- modal for quote report -->
  <b-modal ref="reportQuoteModal"
         id="report-quote-modal"
         title="Report for a quote"
         hide-footer>
  <b-form @submit="onReportSubmit" @reset="onReportReset" class="w-100">
  <b-form-group id="form-quote-group"
                label="Quote:"
                label-for="form-quote-input">
      <b-form-input id="form-quote-input"
                    type="text"
                    v-model="reportQuoteForm.quote"
                    required
                    placeholder="Enter quote">
      </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary" v-b-modal.generate-quote-modal>Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
  </b-modal>

  <!-- modal for adding a quote -->
  <b-modal ref="addQuoteModal"
         id="quote-modal"
         title="Add a new quote"
         hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
  <b-form-group id="form-quote-group"
                label="Quote:"
                label-for="form-quote-input">
      <b-form-input id="form-quote-input"
                    type="text"
                    v-model="addQuoteForm.quote"
                    required
                    placeholder="Enter quote">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-group"
                  label="Author:"
                  label-for="form-author-input">
        <b-form-input id="form-author-input"
                      type="text"
                      v-model="addQuoteForm.author"
                      required
                      placeholder="Enter author">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-date-add-group">
      <b-form-input id="form-date-add-input"
                      type="date"
                      v-model="addQuoteForm.date"
                      required
                      placeholder="Enter date">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-happiness-group"
                  label="Happiness:"
                  label-for="form-happiness-input">
      <b-form-input id="form-happiness-input"
                      type="text"
                      v-model="addQuoteForm.happiness"
                      required
                      placeholder="Enter happiness">
        </b-form-input>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</b-modal>

<!-- modal for updating a quote -->
  <b-modal ref="updateQuoteModal"
         id="update-quote-modal"
         title="Update a quote"
         hide-footer>
  <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
  <b-form-group id="form-quote-update-group"
                label="Quote:"
                label-for="form-quote-update-input">
      <b-form-input id="form-quote-update-input"
                    type="text"
                    v-model="updateQuoteForm.quote"
                    required
                    placeholder="Enter quote">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-update-group"
                  label="Author:"
                  label-for="form-author-update-input">
        <b-form-input id="form-author-update-input"
                      type="text"
                      v-model="updateQuoteForm.author"
                      required
                      placeholder="Enter author">
        </b-form-input>
      </b-form-group>
    <b-form-group id="form-date-update-group">
      <b-form-input id="form-date-update-input"
                      type="date"
                      v-model="updateQuoteForm.date"
                      required
                      placeholder="Enter date">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-happiness-update-group">
      <b-form-input id="form-happiness-update-input"
                      type="number"
                      v-model="updateQuoteForm.happiness"
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
     <button type="button" class="btn btn-success btn-sm" style="margin:5px;" v-b-modal.quote-modal>
       Add Quote</button>
     <button type="button" class="btn btn-success btn-sm" v-b-modal.report-quote-modal>
       Quote Report</button>
    <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Quote</th>
              <th scope="col">Author</th>
              <th scope="col">Date</th>
              <th scope="col">Number Assigned</th>
              <th scope="col">Happiness</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(quote, index) in quotes" :key="index">
              <td>{{ quote.text }}</td>
              <td>{{ quote.author }}</td>
              <td>{{ quote.date }}</td>
              <td>{{ quote.num_assigned }}</td>
              <td>{{ quote.happiness }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.update-quote-modal
                  >Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  v-on:click="deleteQuote(index)">Delete</button>
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
  name: 'Quotes',
  data() {
    return {
      quotes: [],
      quoteusers: [],
      addQuoteForm: {
        quote: '',
        author: '',
        date: '',
        happiness: 0,
      },
      updateQuoteForm: {
        quote: '',
        author: '',
        date: '',
        happiness: 0,
      },
      reportQuoteForm: {
        quote: '',
      },
    };
  },
  methods: {
    getQuotes() {
      const path = 'http://localhost:5000/api/quotes';
      axios.get(path)
        .then((res) => {
          console.log(res.data.quotes);
          this.quotes = res.data.quotes;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addQuote(payload) {
      const path = 'http://localhost:5000/api/quotes/add';
      axios.post(path, payload)
        .then(() => {
          this.getQuotes();
        })
        .catch((error) => {
          console.error(error);
          this.getQuotes();
        });
    },
    deleteQuote(index) {
      const payload = {
        quote: this.quotes[index].text,
        author: this.quotes[index].author,
      };
      const path = 'http://localhost:5000/api/quotes/delete';
      axios.post(path, payload)
        .then(() => {
          this.getQuotes();
        })
        .catch((error) => {
          console.error(error);
          this.getQuotes();
        });
    },
    updateQuote(payload) {
      const path = 'http://localhost:5000/api/quotes/update';
      axios.post(path, payload)
        .then(() => {
          this.getQuotes();
        })
        .catch((error) => {
          console.error(error);
          this.getQuotes();
        });
    },
    reportQuote(payload) {
      const path = 'http://localhost:5000/api/quoteuser';
      axios.post(path, payload)
        .then((res) => {
          this.quoteusers = res.data.quoteusers;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    initForm() {
      this.addQuoteForm.quote = '';
      this.addQuoteForm.author = '';
      this.addQuoteForm.date = '';
      this.addQuoteForm.happiness = 0;
    },
    initUpdateForm() {
      this.updateQuoteForm.quote = '';
      this.updateQuoteForm.author = '';
      this.updateQuoteForm.date = '';
      this.updateQuoteForm.happiness = 0;
    },
    initReportForm() {
      this.reportQuoteForm.quote = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addQuoteModal.hide();
      const payload = {
        quote: this.addQuoteForm.quote,
        author: this.addQuoteForm.author,
        date: this.addQuoteForm.date,
        happiness: this.addQuoteForm.happiness,
      };
      this.addQuote(payload);
      this.initForm();
    },
    onUpdateSubmit(evt) {
      evt.preventDefault();
      this.$refs.updateQuoteModal.hide();
      const payload = {
        quote: this.addQuoteForm.quote,
        author: this.addQuoteForm.author,
        date: this.addQuoteForm.date,
        happiness: this.addQuoteForm.happiness,
      };
      this.updateQuote(payload);
      this.initUpdateForm();
    },
    onReportSubmit(evt) {
      evt.preventDefault();
      this.$refs.reportQuoteModal.hide();
      const payload = {
        quote: this.reportQuoteForm.quote,
      };
      this.reportQuote(payload);
      this.initReportForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addQuoteModal.hide();
      this.initForm();
    },
    onUpdateReset(evt) {
      evt.preventDefault();
      this.$refs.updateQuoteModal.hide();
      this.initUpdateForm();
    },
    onReportReset(evt) {
      evt.preventDefault();
      this.$refs.reportQuoteModal.hide();
      this.initReportForm();
    },
  },
  created() {
    this.getQuotes();
  },
};
</script>
