# Teachable Machine project
# https://teachablemachine.withgoogle.com/models/dT8Zcbt9a/

<div>Teachable Machine Image Model</div>
<button type="button" onclick="init()">Start</button>
<div id="webcam-container"></div>
<div id="label-container"></div>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
<script type="text/javascript">
    // More API functions here:
    // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image

    // the link to your model provided by Teachable Machine export panel
    const URL = "./my_model/";

    let model, webcam, labelContainer, maxPredictions;

    // Load the image model and setup the webcam
    async function init() {
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";

        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // or files from your local hard drive
        // Note: the pose library adds "tmImage" object to your window (window.tmImage)
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();

        // Convenience function to setup a webcam
        const flip = true; // whether to flip the webcam
        webcam = new tmImage.Webcam(200, 200, flip); // width, height, flip
        await webcam.setup(); // request access to the webcam
        await webcam.play();
        window.requestAnimationFrame(loop);

        // append elements to the DOM
        document.getElementById("webcam-container").appendChild(webcam.canvas);
        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) { // and class labels
            labelContainer.appendChild(document.createElement("div"));
        }
    }

    async function loop() {
        webcam.update(); // update the webcam frame
        await predict();
        window.requestAnimationFrame(loop);
    }

    // run the webcam image through the image model
    async function predict() {
        // predict can take in an image, video or canvas html element
        const prediction = await model.predict(webcam.canvas);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction =
                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }
    }
</script>


# Using my Gemini CSC-114 Bot, I asked the following informmation regarding my Teachable Machine Project

# My prompt: 
https://teachablemachine.withgoogle.com/models/dT8Zcbt9a/
here is my simple neural network project.
Why, when teaching to recognize "Image A or B", do we need three states that we train the model to recognize?

# Chatbot response:
When training a machine learning model to recognize "Image A" or "Image B" (such as in Google's Teachable Machine), adding a **third state**—usually called the **Background, Idle, or Neutral state**—is a fundamental best practice.

Here is why that third state is necessary:

### 1. Neural Networks Are Forced to Choose

An image classification model works by calculating probabilities for the classes it has been taught, and those probabilities must always add up to 100%.

If you only train the model on two states (**Class A** and **Class B**), the model has no concept of "nothing" or "neither." It assumes the universe only consists of Class A and Class B. When the camera sees an empty room, your face, or a random object, the model is forced to choose between the two options it knows. As a result, it will output a high-confidence guess for A or B based on completely irrelevant background noise.

### 2. Establishing a Baseline (The "Idle" State)

The third state acts as a baseline or control group. By capturing images of the empty background, the lighting of your room, or your neutral posture, you are teaching the model what the environment looks like when *neither* object is present.

This instructs the model: *"When the camera looks like this, do not trigger A or B."*

### 3. Preventing False Positives

Without a neutral state, your project will suffer from constant false positives.

* **With 2 States:** If Class A is a cup and Class B is a book, an empty frame might be flagged as "Cup: 98%" simply because the color of your wall matches the cup slightly more than the book.
* **With 3 States:** The empty frame will correctly map to the "Background" state with 100% confidence. The model will only switch to "Cup" or "Book" when those distinct features suddenly enter the frame and override the background baseline.

### Summary

In binary classification tasks, a third class is essential for mapping the **"neither" condition**. It ensures your neural network knows how to say "I don't see either of the target objects right now," making your final application far more stable and reliable.


