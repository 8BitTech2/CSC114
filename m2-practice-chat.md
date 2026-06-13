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


# My second interaction
Which type of Teachable Machines model did I make? How well did it seem to do compared to other groups' models?

# Response
## Your Teachable Machine Model Type

Based on your project description of classifying "Image A or B," you built an **Image Project**. Specifically, this is a supervised image classification model that uses transfer learning (built on top of MobileNet) to recognize patterns in visual data from your webcam or uploaded files.

---

## Performance Comparison

As an AI, I can see the structure of your Teachable Machine link, but I cannot directly access the internal weights, training logs, or accuracy metrics stored inside that specific URL (`dT8Zcbt9a`). Furthermore, I don't have access to the private data, models, or projects submitted by the other groups in your class or cohort.

Because of these data privacy boundaries, I can't give you a direct leaderboard comparison. However, in these types of lab environments, the models that consistently outperform the rest usually hit a few specific benchmarks:

* **High Dataset Variance:** If your group took photos from multiple angles, different distances, and varying lighting conditions, your model will heavily outperform groups that took 300 photos of the exact same static frame.
* **A Clean Neutral State:** If you successfully trained that third "background" state we discussed, your model will be significantly more stable (fewer false positives) than groups that skipped it.
* **Balanced Class Sizes:** If your classes had a roughly equal number of sample images (e.g., 200 for A, 200 for B, 200 for Background), your model will be much less biased than a group that gave Class A 500 images and Class B only 50 images.

How did your model handle the live testing preview compared to what you observed from the other groups?

# My third interaction
What skills and workflows do I personally (the student running this prompt) need to develop, in order to work with Python notebooks? (Assume that a IPYNB file is provided by the instructor.)

# Response
To work effectively with Python Notebooks (`.ipynb` files) provided by an instructor, you need to bridge the gap between writing standard code and interacting with a **stateful, cell-based environment**.

Here are the essential skills and workflows you need to develop to hit the ground running:

---

## 1. Core Environmental Skills

### Understanding the "Kernel" and State

Unlike a traditional script that runs from top to bottom and terminates, a notebook runs on a persistent background process called a **Kernel**.

* **The Skill:** Managing the lifecycle of the kernel. You need to know when to restart it to clear memory, or interrupt it if a cell gets stuck in an infinite loop.
* **The Gotcha:** Variable persistence. If you run Cell 3, then go back and change Cell 1, the changes in Cell 1 won't register until you execute it again.

### Cell Execution and Navigation

Notebooks split code and documentation into distinct blocks called cells.

* **Code Cells:** Contain executable Python code.
* **Markdown Cells:** Contain formatted text, equations, and explanations (crucial for academic submissions).
* **Keyboard Shortcuts:** Master `Shift + Enter` (run cell and move to next) and `Ctrl + Enter` (run cell and stay selected). This speeds up your workflow significantly.

---

## 2. Recommended Workflows

### Step 1: Environment Setup

Before you can open the instructor's file, you need a runtime environment. Decide on your primary IDE:

* **The Local Option (Recommended for Privacy/Security):** **VS Code** with the *Jupyter* extension installed. It allows you to run notebooks locally using your machine's Python environment.
* **The Cloud Option:** **Google Colab**. Great for quick access and free GPU acceleration, though it requires uploading the instructor's file to the cloud.

### Step 2: The "Top-to-Bottom" Discipline

Because notebooks allow you to run cells out of order, it is easy to accidentally write "spaghetti state" code that works on your screen but breaks when someone else runs it.

* **The Workflow:** Before submitting any assignment, always use the **"Restart Kernel and Run All Cells"** command. This guarantees your notebook executes flawlessly from a blank slate, which is exactly how your instructor will grade it.

### Step 3: Local Package Management

Instructors often use specific data science or security libraries (e.g., `pandas`, `scikit-learn`, `scapy`) that might not be installed on your machine.

* **The Workflow:** Learn to install missing packages directly inside the notebook using a cell block, or via your terminal environment:
```python
%pip install numpy pandas

```


*(Using `%pip` ensures the package installs directly into the active notebook kernel rather than a random global Python environment).*

### Step 4: Submission Preparation

Instructors rarely grade raw `.ipynb` files directly if they just want to read your analysis.

* **The Workflow:** Master the **Export/Print** workflow. Learn how to convert your finalized notebook into a clean **PDF** or **HTML** file, ensuring all your terminal outputs, charts, and markdown explanations are fully visible without requiring the instructor to rerun your code.

---

Which environment are you planning to use to run these notebooks—VS Code locally, Google Colab, or something else?
