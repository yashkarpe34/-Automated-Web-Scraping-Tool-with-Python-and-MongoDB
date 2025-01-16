// src/components/NewsList.js
import React, { Component } from 'react';
import axios from 'axios';

class NewsList extends Component {
  constructor() {
    super();
    this.state = {
      news: [],
    };
  }

  componentDidMount() {
    axios
      .get('YOUR_NEWS_API_ENDPOINT_HERE')
      .then((response) => {
        this.setState({ news: response.data.articles });
      })
      .catch((error) => {
        console.error('Error fetching news:', error);
      });
  }

  render() {
    return (
      <div>
        <h1>News Articles</h1>
        <ul>
          {this.state.news.map((article) => (
            <li key={article.title}>
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                {article.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default NewsList;
