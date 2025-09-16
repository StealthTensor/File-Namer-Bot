# File Namer Bot 

Yo Ever have a folder full of images with boring names like `IMG_4059.JPG` and a spreadsheet you need to fill out by hand? Yeah, it sucks. This script does all that boring work for you.


## What's this thing do?

Basically, it's a simple workflow:

1.  **Looks at an image** from your `products` folder.
2.  **Asks Google's AI**, "Yo, what is this a picture of?"
3.  **Gets an answer** like "Starry Night by Vincent van Gogh poster".
4.  **Cleans it up** and turns it into a sweet filename like `starry-night-vincent-van-gogh.jpg`.
5.  **Copies the renamed file** over to the `uploaded_products` folder.
6.  **Updates your CSV** with the new filename and a proper name.
7.  Does this for **ALL** your images. Boom. Done. 

## How to Use It 


### 1\. Download the code

Clone this repo or just download it as a ZIP file.

```bash
git clone https://github.com/StealthTensor/File-Namer-Bot.git
```

### 2\. Install the necessary stuff

You'll need Python, obviously. Then open your terminal or command prompt and run this:

```bash
pip install pandas google-cloud-vision
```

### 3\. The Google AI Thing (IMPORTANT\!)

This is the only tricky part. The script needs a key to talk to Google's AI.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (or use one you already have).
3.  Make sure you **Enable the Cloud Vision API** for that project.
4.  Create a "Service Account". When you create it, give it a role like "Viewer" or "Editor".
5.  Generate a JSON key for that service account and download it.
6.  *RENAME THE DOWNLOADED FILE* to `service-account-key.json` and put it in the same folder as the `run_automation.py` script.

 Google might ask you to enable billing. The Vision AI has a free tier which is pretty generous, but they still need a card on file just in case.

### 4\. Set up your folders and files

Your project folder needs to look exactly like this:

```
your-project-folder/
├── products/
│   └── your-image-1.jpg
│   └── another-pic.png
│   └── ... (put all your images here)
├── uploaded_products/  <-- (create this folder, it can be empty)
├── products.csv        <-- (your spreadsheet with 'Name' and 'Slug' columns)
├── run_automation.py
├── service-account-key.json
└── credentials.json
```

### 5\. Run it\!

Just open your terminal in the project folder and type:

```bash
python run_automation.py
```

Now sit back and watch the magic happen\! It will print its progress for each file. When it's done, you'll have a new file called `products_updated.csv` with all the new info.

## What's all this stuff? 

  * `run_automation.py`: The main script with all the code.
  * `products/`: The folder where you dump all your images that need renaming.
  * `uploaded_products/`: The folder where the script saves the newly named images.
  * `products.csv`: Your starting spreadsheet. It needs at least a `Name` and `Slug` column.
  * `products_updated.csv`: The new spreadsheet the script makes with all the updated names.
  * `service-account-key.json`: Your secret key to connect to the Google AI. **Don't share this or upload it to GitHub\!**
  * `credentials.json`: Looks like another key file, probably for something else. This script doesn't use it.
