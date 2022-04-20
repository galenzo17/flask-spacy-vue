
<template>
  <div class="hello">
    <div class="navigatorapibutons">
      <i class="material-icons md-60" @click="initCaptureAudio"> mic </i>
      <i class="material-icons" @click="recorderstop"> stop_circle </i>
      <i class="material-icons md-60" @click="openFile"> attachment </i>
      <i class="material-icons md-60" @click="initCapture"> videocam </i>
    </div>
    <img
      v-show="imageUrl != ''"
      v-bind:src="imageUrl"
      ref="output"
      class="pasteimagepreview"
    />
    <div class="textareacard">
      <textarea
        placeholder="Ingresa tu nota o puedes pegar una imagen,o grabar un audo o subir un archivo..."
        ref="target"
        rows="5"
        cols="33"
      ></textarea>
    </div>

    <input
      name="file"
      type="file"
      ref="superinput"
      enctype="multipart/form-data"
      style="display: none"
      @change="uploadFile"
    />
    <div class="footerformcard">
      <div class="savebutondiv" @click="save">
        <i class="material-icons md-60"> save </i>Guardar
      </div>
    </div>
    <video ref="player" v-show="imageUrl != ''" controls autoplay></video>
    <canvas ref="canvas" style="display: none"></canvas>
    <div ref="playeraudio"></div>
    <div class="notescontainer">
      <div class="notecontainer" v-for="note in notes" v-bind:key="note.id">
        <div class="notedate">{{ note.date }}</div>
        <div class="noteheader">
          {{ note.text }}
        </div>
        <div class="notefooter">
          <div
            v-for="tag in note.tags"
            v-bind:key="tag.id"
            href="#"
            class="badgeoldschool"
          >
            {{ tag.tag }}
            <div class="detalleamount">{{ tag.valor }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div
  id="svgcontainer">

      </div>
      <div
  id="svgcontainer2">

      </div>
    </div>
    <!--
    <button ref="capture">Capture</button>
    <button ref="initcapture">Init Capture</button>!-->
    <!-- <button ref="recorder" @click="initCaptureAudio">Capture Audio</button>
    <button ref="recorderstop" @click="recorderstop">Stop Audio</button> -->
  </div>
</template>

<script>
import axios from "axios";
import { pan, zoom, getScale, setScale, resetScale } from 'svg-pan-zoom-container';
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Una nota con super poderes...",
      document: document,
      imageUrl: "",
      audioChunks: [],
      mediaRecorder: "",
      notes: [],
    };
  },
  methods: {
    getTransformParameters: function (element) {
        console.log(element);
      const transform = element.style.transform;
      let scale = 1,
        x = 0,
        y = 0;

      if (transform.includes("scale"))
        scale = parseFloat(transform.slice(transform.indexOf("scale") + 6));
      if (transform.includes("translateX"))
        x = parseInt(transform.slice(transform.indexOf("translateX") + 11));
      if (transform.includes("translateY"))
        y = parseInt(transform.slice(transform.indexOf("translateY") + 11));

      return { scale, x, y };
    },

    getTransformString:function (scale, x, y) {

        return "scale(" + scale + ") " + "translateX(" + x + "%) translateY(" + y + "%)"
    },
    pan:function (direction)  {
      const { scale, x, y } = this.getTransformParameters(svg);
      let dx = 0,
        dy = 0;
      switch (direction) {
        case "left":
          dx = -3;
          break;
        case "right":
          dx = 3;
          break;
        case "up":
          dy = -3;
          break;
        case "down":
          dy = 3;
          break;
      }
      svg.style.transform = this.getTransformString(scale, x + dx, y + dy);
    },

    zoom: function (direction)  {
      const { scale, x, y } = this.getTransformParameters(svg);
      let dScale = 0.1;
      if (direction == "out") dScale *= -1;
      if (scale == 0.1 && direction == "out") dScale = 0;
      svg.style.transform = this.getTransformString(scale + dScale, x, y);
    },
    save() {
      console.log("save");
      if (this.$refs.target.value == "") {
        alert("Debes ingresar una nota o una imagen o un audio");
        return;
      }

      var text = this.$refs.target.value;
      let formData = new FormData();
      formData.append("text", text);

      axios
        .post("http://127.0.0.1:5000/api/v1.0/prediction", formData)
        .then((response) => {
            console.log(response);
            const svg = document.getElementById("svgcontainer");
    console.log(svg);
    svg.innerHTML += response.data.testtodisplaydep
    const svg2 = document.getElementById("svgcontainer");
    console.log(svg2);
    svg2.innerHTML += response.data.testtodisplayent
          let tagid = 0;
          let tags = [];
          response.data.textToFive.forEach((tag) => {
            console.log(tag);
            //first key of tag
            let llave = "";
            let valor = "";
            for (var i in tag) {
              llave = i; // alerts key
              valor = tag[i]; //alerts key's value
            }
            tags.push({
              tag: llave,
              valor: valor,
              id: tagid++,
            });
          });

          //console.log(tags);
          this.notes.push({
            date: new Date().toLocaleString(),
            text: this.$refs.target.value,
            tags: tags,
          });
          this.$refs.target.value = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
    openFile() {
      this.$refs.superinput.click();
    },
    uploadFile(e) {
      // e.preventDefault();
      console.log("uploadFile");
      //this.$refs["superinput"].click();
      const path = "http://127.0.0.1:5000/api/v1.0/prediction";
      let file = this.$refs.superinput.files[0];
      let formData = new FormData();
      formData.append("file", file);
      axios.post(path, formData).then((response) => {
        this.imageUrl = response.data.url;
      });
    },
    getMensaje() {
      const path = "http://127.0.0.1:5000/api/v1.0/mensaje";
      axios
        .get(path)
        .then((resp) => {
          console.log(resp);
          this.msg = resp.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    doSomethingWithFiles(fileList) {
      console.log(fileList);
      const output = this.$refs.output;
      let file = null;

      for (let i = 0; i < fileList.length; i++) {
        if (fileList[i].type.match(/^image\//)) {
          file = fileList[i];
          break;
        }
      }

      if (file !== null) {
        console.log(file);
        this.imageUrl = URL.createObjectURL(file);
        output.src = URL.createObjectURL(file);
      }
    },
    initCapture() {
      console.log("captura");
      const player = this.$refs.player;
      const canvas = this.$refs.canvas;
      canvas.width = player.videoWidth;
      canvas.height = player.videoHeight;
      const context = this.$refs.canvas.getContext("2d");
      const captureButton = this.$refs.capture;
      const constraints = {
        video: true,
      };

      captureButton.addEventListener("click", () => {
        context.drawImage(player, 0, 0, canvas.width, canvas.height);

        // Stop all video streams.
        player.srcObject.getVideoTracks().forEach((track) => track.stop());
      });

      navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        // Attach the video stream to the video element and autoplay.
        console.log(stream);
        this.imageUrl = stream;
        player.srcObject = stream;
      });
    },
    initCaptureAudio() {
      //console.log("captura audio");
      var app = this;
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        app.mediaRecorder = new MediaRecorder(stream);
        app.mediaRecorder.start();

        const audioChunks = [];
        app.mediaRecorder.addEventListener("dataavailable", (event) => {
          app.audioChunks.push(event.data);
        });

        app.mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(app.audioChunks, {
            type: "audio/wav",
          });
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          audio.setAttribute("controls", 1);
          this.$refs.playeraudio.appendChild(audio);
          audio.play();
          var fd = new FormData();
          fd.append("fname", "test.wav");
          fd.append("file", audioBlob);
          const path = "http://127.0.0.1:5000/api/v1.0/prediction";
          axios.post(path, fd).then((response) => {
            file: fd;
          });
          stream
            .getTracks() // get all tracks from the MediaStream
            .forEach((track) => {
              console.log("hola track", track);
              track.stop();
            });
          console.log("stop audio", audioBlob);
        });
      });
    },
    recorderstop() {
      console.log(this.mediaRecorder);
      this.mediaRecorder.stop();

      // const player = this.$refs.playeraudio;
      // player.srcObject.getAudioTracks().forEach(track => track.stop());
    },
  },
  mounted() {
    const initcaptureButton = this.$refs.initcapture;
    const initcaptureButtonaudio = this.$refs.recorder;
    // initcaptureButtonaudio.addEventListener("click", this.initCaptureAudio);
    //this.mediarecord_tmp=navigator.mediaDevices
    //this.getMensaje()
    //console.log(this.mediarecord_tmp);
    const svg = document.getElementById("svg");
    console.log(svg);
    // document.getElementById("left-button").onclick = () => this.pan("left");
    // document.getElementById("right-button").onclick = () => this.pan("right");
    // document.getElementById("up-button").onclick = () => this.pan("up");
    // document.getElementById("down-button").onclick = () => this.pan("down");

    // document.getElementById("zoom-in-button").onclick = () => this.zoom("in");
    // document.getElementById("zoom-out-button").onclick = () => this.zoom("out");
    this.$nextTick(() => {
      //this.initCapture();
      // this.$refs["superinput"].addEventListener(
      //   "change",
      //   this.uploadFile()
      // );
    });
    this.$refs.target.addEventListener("paste", (e) => {
      //e.preventDefault();
      this.doSomethingWithFiles(e.clipboardData.files);
    });

    // initcaptureButton.addEventListener("click", () => {
    //   this.initCapture();
    // });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.displacy{
    width: 90%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
}
.detalleamount {
  background-color: black;
  color: white;
  border-radius: 50%;
  padding: 10px;
}
.badgeoldschool {
  border-radius: 50px;
  padding: 5px;
  background-color: rgb(163, 236, 194);
  color: rgb(134, 134, 134);
}
.notedate {
  border-radius: 4px;
  padding: 10px;
  background-color: rgb(233, 187, 187);
}
.noteheader {
}
.notefooter {
  display: flex;
  justify-content: space-around;
  flex-wrap: nowrap;
}
.notecontainer {
  margin: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
.notescontainer {
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  padding: 15px;
}
.navigatorapibutons :hover {
  color: rgb(81, 159, 204);
}
.savebutondiv {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
}
.savebutondiv:hover {
  background-color: #ccc;
}
.footerformcard {
  display: flex;
  justify-content: flex-end;
}
textarea {
  width: 100%;
  height: 150px;
  padding: 12px 20px;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  font-size: 16px;
  resize: none;
}
@font-face {
  font-family: "Material Icons";
  font-style: normal;
  font-weight: 400;
}
.material-icons {
  font-family: "Material Icons";
  font-weight: normal;
  font-style: normal;
  font-size: 24px; /* Preferred icon size */
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;

  /* Support for all WebKit browsers. */
  -webkit-font-smoothing: antialiased;
  /* Support for Safari and Chrome. */
  text-rendering: optimizeLegibility;

  /* Support for Firefox. */
  -moz-osx-font-smoothing: grayscale;

  /* Support for IE. */
  font-feature-settings: "liga";
}
</style>
