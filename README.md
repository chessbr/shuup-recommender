# Shuup Recommender

A complete and open source recommender system for Shuup.

The recommener system provides a powerful API to use the recommendations anywhere, be it in admin, frontend templates or also through REST APIs.

# Documentation

TODO

# Features

Work in progress.

# TODOs

Here is the list of features to be implemented in the first release:

- [ ] Popularity: a simple rank of most seen products.
- [ ] Who bought this, also bought: suggest products based on product purchase history of other customers using collaborative filtering. Features like age, gender etc might be useful when ranking the products. User-based filtering.
- [ ] Who saw this, also saw: suggest products based on product visit history of other customers using collaborative filtering. Features like age, gender etc might be useful when ranking the products. Item-based filtering.
- [ ] Category similarity: suggest categories to be used in products based on the product name and description. Used especially in admin to help with product creation task. Content-based filtering.
- [ ] Product similarity: suggest products that are similar based on product images and/or name/description/categories. Can be used in frontend and also in admin. Content-based filtering.

# Development

Use Jupyter notebooks to create the models before adding methods into the API.

To create or modify noteboks, install Jupyer: `pip install jupyter`

Then run it using notebooks path using this command at project root path: `jupyter notebook --notebook-dir notebooks/`

# License

Apache 2.0
