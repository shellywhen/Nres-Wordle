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
    <el-form :model="data_form" ref="data_form" label-width="90px" size="mini">



      <el-row>
        <el-col :span="5">
          <el-form-item label="Split" prop="need_truncate">
            <el-switch v-model="data_form.need_truncate"></el-switch>
          </el-form-item>
        </el-col>
        <el-col :span="19">
          <el-form-item label="Scale" prop="scale">
            <el-radio-group v-model="data_form.scale" v-bind="data_form.scale" value="linear">
              <el-radio label="Linear" value="linear"></el-radio>
              <el-radio label="Log" value="log"></el-radio>
              <el-radio label="Exponential" value="exp"></el-radio>
              <el-radio label="Square Root" value="sqrt"></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>

      </el-row>

      <el-row :gutter="0">
        <el-col :span="5">
          <div class="grid-content bg-purple"><span>Canvas Resolution</span></div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Width" prop="width">
              <el-input type="number" v-model="data_form.width" placeholder="1960" min="200" max="20000"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="1"> <span class="fake"> - </span></el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Height" prop="height">
              <el-input type="number" v-model="data_form.height" placeholder="1080" min="200" max="20000"></el-input>
            </el-form-item>
            <el-col :span="1"> <span class="recommend"></span></el-col>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="0">
        <el-col :span="5">
          <div class="grid-content bg-purple"><span>Large Wordle</span></div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Max" prop="outer_max_font_size">
              <el-input type="number" v-model="data_form.outer_max_font_size" placeholder="512" min="80" max="1200"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="1"> <span class="recommend">{{re_outer_max}}</span></el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Min" prop="outer_min_font_size">
              <el-input type="number" v-model="data_form.outer_min_font_size" placeholder="64" min="30" max="500"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="1"> <span class="recommend">{{re_outer_min}}</span></el-col>
        <el-col :span="7">
          <div class="grid-content bg-purple">
            <el-form-item label="Font" prop="outer_font">
              <el-select v-model="data_form.outer_font" placeholder="Select Font">
                <el-option v-for="option in font_list" v-bind:key="option.path" v-bind:value="option.path" v-bind:label="option.name">
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="0">
        <el-col :span="5">
          <div class="grid-content bg-purple"><span>Tiny Wordle</span></div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Max" prop="inner_min_font_size">
              <el-input type="number" v-model="data_form.inner_max_font_size" placeholder="32" min="4" max="200"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="1"> <span class="recommend">{{re_inner_max}}</span></el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Min" prop="inner_min_font_size">
              <el-input type="number" v-model="data_form.inner_min_font_size" placeholder="12" min="4" max="200"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="1"> <span class="recommend">{{re_inner_min}}</span></el-col>
        <el-col :span="7">
          <div class="grid-content bg-purple">
            <el-form-item label="Font" prop="inner_font">
              <el-select v-model="data_form.inner_font" placeholder="Select Font">
                <el-option v-for="option in font_list" v-bind:key="option.name" v-bind:value="option.path" v-bind:label="option.name">
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row>

      <!-- <el-row :gutter="0">
        <el-col :span="5">
          <div class="grid-content bg-purple"><span>Style</span></div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <div class="grid-content bg-purple">
              <el-form-item label="Large Font" prop="outer_font">
                <el-select v-model="data_form.outer_font" placeholder="Select Font">
                  <el-option v-for="option in font_list" v-bind:key="option.name" v-bind:value="option.path" v-bind:label="option.name">
                  </el-option>
                </el-select>
              </el-form-item>
            </div>
          </div>
        </el-col>
        <el-col :span="1"> <span class="fake">-</span></el-col>
        <el-col :span="5">
          <div class="grid-content bg-purple">
            <el-form-item label="Tiny Font" prop="inner_font">
              <el-select v-model="data_form.inner_font" placeholder="Select Font">
                <el-option v-for="option in font_list" v-bind:key="option.name" v-bind:value="option.path" v-bind:label="option.name">
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
      </el-row> -->


      <el-row>
        <el-col :span="5">
          <span class="normal-label">Blend</span>
        </el-col>
        <el-col :span="2">
          <span class="normal-label">Blur</span>
        </el-col>
        <el-col :span="7">
          <div class="block">
            <el-slider v-model="data_form.radius" show-input input-size="mini" :min="0" :max="data_form.outer_min_font_size" :step="1" :value="data_form.radius">
            </el-slider>
          </div>
        </el-col>
        <el-col :span="1">
          <span class="fake">&</span>
        </el-col>

        <el-col :span="2">
          <span class="normal-label">Alpha</span>
        </el-col>
        <el-col :span="7">
          <div class="block">
            <el-slider v-model="data_form.blend_alpha" show-input input-size="mini" :min="0" :max="1" :step="0.01" :v-model="data_form.blend_alpha">
            </el-slider>
          </div>
        </el-col>
      </el-row>



      <el-row>
        <el-col :span="5">
        </el-col>
        <el-col :span="5">
        </el-col>
        <el-col :span="1">
        </el-col>
        <el-col :span="5">
        </el-col>
        <el-col :span="1">
        </el-col>
        <el-col :span="7">
        </el-col>
      </el-row>


      <el-form-item>
        <el-button type="primary" plain @click="preview();">Preview <i class="el-icon-view"></i></el-button>
        <el-button type="success" plain @click="submitForm('ruleForm')">Create <i class="el-icon-check"></i></el-button>
        <el-button tyle="info" plain @click="resetForm('ruleForm')">Reset <i class="el-icon-refresh-right"></i></el-button>
          <el-button size="mini" plain @click="openFile">Font&nbsp;<i class="el-icon-upload2"></i></el-button>
          <span class="el-radio__label flex-span">{{data_form.filename}}</span>
          <input type="file" name="file_input" class="file_input" style="display: none" />
      </el-form-item>
    </el-form>

    <el-dialog title="Wordle is Ready 😉" :visible.sync="dialogVisible" width="30%" :before-close="handleCloseDialog">
      <span>Download the Generated Wordcloud.</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleDownloadImage">Download</el-button>
      </span>
    </el-dialog>
  </div>
  <div class="block" style="text-align:middle;width:100%;">
  <el-image  :width="canvas.width" :height="canvas.height" :src="preview_img">
    <div slot="error" :style="{width:canvas.width,height:canvas.height}" class="image-slot">
      <span class="vertical-helper"></span><i class="el-icon-picture-outline vertical-icon"></i>
    </div>
  </el-image>
</div>
</div>
</template>

<script>
// @ is an alias to /src
import * as axios from 'axios'
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
export default {
  name: 'Form',
  data() {
    return {
      preview_img: `${this.$hostname}+'/preview_img.png'`,
      canvas: {
        height: '200px',
        width: '500px'
      },
      image: "",
      file: "",
      font_list: [{
        name: 'Arial',
        path: 'font/arial.ttf'
      }, {
        name: 'Sans Serif',
        path: 'font/sans-serif.ttf'
      }],
      data_form: {
        type: "copy",
        paste: "",
        url: "",
        filename: "",
        processedData: {},
        width: 1960,
        height: 1080,
        outer_max_font_size: 250,
        outer_min_font_size: 64,
        inner_max_font_size: 45,
        inner_min_font_size: 8,
        inner_repeat: false,
        blend_alpha: 0.7,
        radius: 10,
        background_color: 'white',
        outer_font_path: 'font/msyh.ttf',
        inner_font_path: 'font/msyh.ttf',
        need_truncate: false,
        scale: 'linear'
      },
      dialogVisible: false
    }
  },
  mounted() {
    let self = this
    window.$('.file_input').on('change', function(e) {
      let file = e.target.files[0]
      console.log(file)
      self.data_form.filename = file.name
      self.data_form.file = file
    })
  },
  computed: {
    re_outer_min() {
      return 64
    },
    re_outer_max() {
      return 256
    },
    re_inner_min() {
      return 16
    },
    re_inner_max() {
      return 32
    }
  },
  methods: {
    preview() {
      console.log(this.ruleForm)
      axios.post(this.$hostname + '/preview', this.data_form)
        .then(response => {
          this.processedData = response.data
          this.dialogVisible = true
          console.log(this, response.data)
        })
        .catch(error => console.log(error));
    },
    submitForm(form) {
      console.log(form)
      axios.post(this.$hostname + '/dataHandler', form)
        .then(response => {
          this.processedData = response.data
          this.dialogVisible = true
          console.log(this, response.data)
        })
        .catch(error => console.log(error));
    },
    handleTabClick(tab, event) {
      console.log(tab, event)
    },
    handleCloseDialog() {
      this.dialogVisible = false
    },
    handleDownloadImage() {
      console.log('download')
      this.dialogVisible = false
      window.location = this.$hostname + '/generated/wordle.jpg'
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
    margin: 2vh auto auto;
}
.form-wrapper {
    text-align: center;
    width: 100%;
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

.recommend {
    color: #088f57;
    display: flex;
    line-height: 2;
    padding-left: 4px;
}

.el-input__inner {
    padding: 0 0 0 15px;
}

.fake {
    color: white;
}

.normal-label {
  line-height: 3;
}

.el-input-number--mini .el-input__inner {
    padding-left: 15px;
    padding-right: 15px;
}
.image-slot {
  background-color: #F2F6FC;
  text-align: center;
}

.vertical-helper {
  text-align: center;
  display: inline-block;
  height:100%;
  vertical-align: middle;
}
.vertical-icon {
   vertical-align: middle;
   max-height: 3rem;
   max-width: 3rem;
   font-size: 3rem;
}

.create {
  text-align: center;
}
</style>
