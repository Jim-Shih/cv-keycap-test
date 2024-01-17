<template>
    <div>
        <button @click="checkHealth">Check API Health</button>
        <p v-if="apiHealthStatus">API Health Status: {{ apiHealthStatus }}</p>
        <input type="file" @change="uploadImage" />
        <div class="image-container">
            <img
                :src="uploadedImage"
                alt="Uploaded Image"
                v-if="uploadedImage"
                class="half-width"
            />
            <img
                :src="processedImage"
                alt="Processed Image"
                v-if="processedImage"
                class="half-width"
            />
        </div>
    </div>
</template>

<script>
import axios from "axios";
const backend_port = process.env.VUE_APP_BACKEND_PORT;
const version_number = process.env.VUE_APP_VERSION_NUMBER;

// modify the default url to point to your API server
axios.defaults.baseURL = `http://localhost:${backend_port}`;
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.post["Accept"] = "application/json";

const checkHealth = function () {
    axios
        .get(`/api/v${version_number}/health_check`)
        .then((response) => {
            this.apiHealthStatus = response.data.status;
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
        });
};

const uploadImage = function (event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = () => {
        this.uploadedImage = reader.result;
        var base64Image = reader.result;
        // Send the base64 encoded image to the server for processing
        axios
            .post(
                `/api/v${version_number}/preprocessing`,
                JSON.stringify({ base64_string: base64Image }),
            )
            .then((response) => {
                this.processedImage =
                    "data:image/png;base64," + response.data.processedImage;
            })
            .catch((error) => {
                console.error(error);
            });
    };

    reader.readAsDataURL(file);
};

export default {
    data() {
        return {
            uploadedImage: null,
            processedImage: null,
            apiHealthStatus: null,
        };
    },
    methods: {
        checkHealth,
        uploadImage,
    },
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>

<style scoped>
.half-width {
    width: 50%;
}

.image-container {
    display: flex;
    flex-wrap: wrap;
}
</style>
