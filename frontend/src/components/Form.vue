<template>
  <div class="form-wrapper">
    <div class="form">
      <el-tabs v-model="data_form.type" @tab-click="handleTabClick">
        <el-tab-pane label="Copy & Paste" name="copy">
          <div class="input-wrapper">
          <el-input placeholder="input the url for the corpus" v-model="data_form.url" size="mini">
                      <template slot="prepend">URL</template>
          </el-input>
        </div>
        <div>
          <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 4}" placeholder="copy and paste the corpus directly" v-model="data_form.paste">
          </el-input>
        </div>
        </el-tab-pane>
    <el-tab-pane label="File" name="file">
      <div style="margin-bottom: 0.5vh;">
      <span class="flex-span">Upload the source from PDF/TXT or a JSON formatted specification.</span>
    </div>
      <div class="flex-line">
      <el-button size="mini" plain @click="openFile">Upload&nbsp;<i class="el-icon-upload el-icon-right"></i></el-button>
       <span class="el-radio__label flex-span">{{data_form.filename}}</span>
      <input type="file" name="file_input" class="file_input" style="display: none" />
    </div>
    </el-tab-pane>
  </el-tabs>
</div>

<div class="form">
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="ruleForm" size="mini">
  <el-form-item label="Activity name" prop="name">
    <el-input v-model="ruleForm.name"></el-input>
  </el-form-item>
  <el-form-item label="Activity zone" prop="region">
    <el-select v-model="ruleForm.region" placeholder="Activity zone">
      <el-option label="Zone one" value="shanghai"></el-option>
      <el-option label="Zone two" value="beijing"></el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="Activity time" required>
    <el-col :span="11">
      <el-form-item prop="date1">
        <el-date-picker type="date" placeholder="Pick a date" v-model="ruleForm.date1" style="width: 100%;"></el-date-picker>
      </el-form-item>
    </el-col>
    <el-col class="line" :span="2">-</el-col>
    <el-col :span="11">
      <el-form-item prop="date2">
        <el-time-picker placeholder="Pick a time" v-model="ruleForm.date2" style="width: 100%;"></el-time-picker>
      </el-form-item>
    </el-col>
  </el-form-item>
  <el-form-item label="Instant delivery" prop="delivery">
    <el-switch v-model="ruleForm.delivery"></el-switch>
  </el-form-item>
  <el-form-item label="Activity type" prop="type">
    <el-checkbox-group v-model="ruleForm.type">
      <el-checkbox label="Online activities" name="type"></el-checkbox>
      <el-checkbox label="Promotion activities" name="type"></el-checkbox>
      <el-checkbox label="Offline activities" name="type"></el-checkbox>
      <el-checkbox label="Simple brand exposure" name="type"></el-checkbox>
    </el-checkbox-group>
  </el-form-item>
  <el-form-item label="Resources" prop="resource">
    <el-radio-group v-model="ruleForm.resource">
      <el-radio label="Sponsorship"></el-radio>
      <el-radio label="Venue"></el-radio>
    </el-radio-group>
  </el-form-item>
  <el-form-item label="Activity form" prop="desc">
    <el-input type="textarea" v-model="ruleForm.desc"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm('ruleForm')">Create</el-button>
    <el-button @click="resetForm('ruleForm')">Reset</el-button>
  </el-form-item>
</el-form>
<el-dialog title="Wordle is Ready 😉" :visible.sync="dialogVisible"
  width="30%"
  :before-close="handleCloseDialog">
  <span>Download the Generated Wordcloud.</span>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">Cancel</el-button>
    <el-button type="primary" @click="handleDownloadImage">Download</el-button>
  </span>
</el-dialog>
</div>
</div>

</template>

<script>
// @ is an alias to /src
import * as axios from 'axios'
axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
export default {
  name: 'Form',
  data() {
     return {
       image: "",
       file: "",
       data_form: {
         type: "copy",
         paste: "",
         url: "",
         filename: "",
         processedData: {}
       },
       ruleForm: {
         name: '',
         region: '',
         date1: '',
         date2: '',
         delivery: false,
         type: [],
         resource: '',
         desc: ''
       },
       dialogVisible: false
     }
   },
 mounted() {
   let self = this
   window.$('.file_input').on('change', function(e) {
     let file = e. target.files[0]
     console.log(file)
     self.data_form.filename = file.name
     self.data_form.file = file
   })
 },
 methods: {
    submitForm() {
      $.ajax({
          type: 'POST',
          contentType: 'multipart/form-data',
          url: this.$hostname + '/dataHandler',
          data : {
            file: this.file,
            data: JSON.stringify(this.data_form)
          },
          success : function(result) {
            console.log(result)
          },error : function(result){
             console.log(result);
          }
      })
      axios.post(this.$hostname+'/dataHandler', this.data_form)
        .then(response => {
          this.processedData = response.data
          this.dialogVisible = true
          console.log(this, response.data)
        })
        .catch(error => console.log(error));
    },
    handleTabClick(tab, event) {
    },
    handleCloseDialog() {
      THIS.dialogVisible = false
    },
    handleDownloadImage() {
      console.log('download')
      this.dialogVisible = false
      window.location = this.$hostname+'/generated/wordle.jpg'
    },
    openFile() {
      console.log('click')
       window.$('.file_input').trigger('click')
    }
  }
}
</script>
<style lang="less">
.form {
  text-align: left;
  width: 80vw;
    margin: auto;
    margin-top: 2vh;
}
.form-wrapper {
  text-align: center;
  width: 99vw;
}
.input-wrapper {
  margin-bottom: 18px;
}
.flex-line {
  display: flex;
}
.flex-span {
  margin-top: auto;
  margin-bottom: auto;
}
.form {
  font-size: 14px;
}
</style>
