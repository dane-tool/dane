# How to develop this website

To develop this locally, a couple steps need to be taken:

1. Install ruby

    I found this the most helpful: https://jekyllrb.com/docs/installation/ubuntu/

    Make sure to run the bashrc steps if you want to install gems locally rather than system-wide.

    Then run the `gem install jekyll bundler` step.

2. Add a Gemfile to this directory (/docs). Just `touch Gemfile`, no need to have any content.
3. Run `gem install github-pages jekyll-remote-theme`
4. Run `gem install jekyll-rtd-theme --version "2.0.10" --source "https://rubygems.pkg.github.com/rundocs"`
5. Run `bundle add github-pages jekyll-remote-theme jekyll-rtd-theme`

When you want to look at the site, run `bundle exec jekyll serve --livereload`.

See https://github.com/rundocs/jekyll-rtd-theme for the theme and configuration options.

In general, if there is some component you want changed just find the liquid file which defines it and overwrite it (e.g. add a new file to `_includes/...`, copy the contents from the repo, and edit the lines you want changed.)
