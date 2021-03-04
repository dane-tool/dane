# How to develop this website

To develop this locally, a couple steps need to be taken:

1. Install ruby

    I found this the most helpful: https://jekyllrb.com/docs/installation/ubuntu/

    Make sure to run the bashrc steps if you want to install gems locally rather than system-wide.

    Then run the `gem install jekyll bundler` step.

2. Add a Gemfile to this directory (/docs). Just `touch Gemfile`, no need to have any content.
3. Run `gem install github-pages jekyll-remote-theme`
4. Run `bundle add github-pages jekyll-remote-theme`

When you want to look at the site, run `bundle exec jekyll serve`.

There are currently some issues to work out with the remote theme. The site builds just fine the first time around, but after it watches a change it complains that it can't find the remote theme. For now we just interrupt and re-run the serve command whenever we want to see a change!

See https://github.com/rundocs/jekyll-rtd-theme for the theme.
