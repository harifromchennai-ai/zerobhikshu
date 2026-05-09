# How to Update the Website

This guide provides manual steps for adding articles and photo galleries to the website.

## 1. How to Add a New Article

1.  **Locate the Template:** Open `docs/_templates/article-template.md`.
2.  **Create a New File:** In the `docs/_posts` folder, create a new file named `YYYY-MM-DD-your-title.md` (e.g., `2026-06-15-summer-solstice.md`).
3.  **Copy the Template:** Copy the contents of the article template into your new file.
4.  **Edit the Content:**
    *   Change the `title:` in the top section (between the `---` dashes).
    *   Change the `date:` to the current date and time.
    *   Write your article below the dashes.
5.  **Save:** Once you save and commit the file to GitHub, it will automatically appear on the **Articles** page!

## 2. How to Add a New Photo Gallery

1.  **Upload Images:** Copy your new photos into the `docs/assets/images/` folder.
2.  **Locate the Template:** Open `docs/_templates/gallery-template.md`.
3.  **Create a New Gallery Page:** In the `docs/` folder, create a new Markdown file for your gallery (e.g., `docs/gallery-retreat-2026.md`).
4.  **Copy the Template:** Copy the contents of the gallery template into your new file.
5.  **Edit the Content:**
    *   Update the `title:` and headings.
    *   Replace the placeholder image links with the actual names of the photos you uploaded in step 1. For example: `![Group Photo](/assets/images/my-new-photo.jpg)`.
6.  **Link to the New Gallery:** Open `docs/photos.md` and add a new link pointing to your newly created gallery page. Use this format at the bottom of the page:

```html
<a href="{{ '/gallery-retreat-2026.html' | relative_url }}" class="photo-gallery-link">
  <h3>Retreat 2026</h3>
  <p>Photos from our wonderful 2026 summer retreat.</p>
</a>
```

## 3. How to Update the Logo or Header Image
If you need to change the main site images in the future:
1. Place the new image in `docs/assets/images/`.
2. To update the main background, edit `docs/assets/css/style.css` and change the `url('../images/pathajaliwithguru.png')`.
3. To update the top banner, edit `docs/assets/css/style.css` and change `url('../images/guruLogo.png')`.
4. To update the circular logos, edit `docs/_layouts/default.html` and change the paths pointing to `logo.jpg`.