[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  
  <h3 align="center">A CBT(RESTful api) app created with Django</h3>
  
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

A simple computer based test web application that allows owners to create examinations, add questions to it and randomly present the questions and its answer options to different exam takers. On the other hand, allows taker to take these exams and also view their results thereafter. The APIs would be consumed with Vue and React and would poses other functionalities.

### Built With

* [Django](https://djangoproject.com)
* [DjangoRestFramework](https://www.django-rest-framework.org/)


<!-- GETTING STARTED -->
## Getting Started

We have simple basic steps that can be performed to get us started.

### Installation (Backend)

1. Clone the repo
   ```sh
   git clone https://github.com/harryface/cbt-django-backend.git
   ```
2. Create a virtual environment on your local system
   ```sh
   python -m venv <path/to/virtual environment>
   ```
3. Install all dependencies in `requirements.txt`
   ```sh
   pip install -r requiremnets.txt
   ```
4. Create the database
   ```sh
   python manage.py makemigrations
   ```
   ```sh
   python manage.py migrate
   ```
5. Run the app
   ```sh
   python manage.py runserver
   ```

<!-- ENDPOINT EXAMPLES -->
## Endpoints

`coming soon`



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Harry Ilonze - harryilonze@yahoo.com

Project Link: [https://github.com/harryface/cbt-django-backend](https://github.com/harryface/cbt-django-backend)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Othneil Drew](https://github.com/othneildrew/Best-README-Template)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[forks-shield]: https://img.shields.io/github/forks/harryface/cbt-django-backend.svg?style=for-the-badge
[forks-url]: https://github.com/harryface/cbt-django-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/harryface/cbt-django-backend.svg?style=for-the-badge
[stars-url]: https://github.com/harryface/cbt-django-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/harryface/cbt-django-backend.svg?style=for-the-badge
[issues-url]: https://github.com/harryface/cbt-django-backend/issues
[license-shield]: https://img.shields.io/github/license/harryface/cbt-django-backend.svg?style=for-the-badge
[license-url]: https://github.com/harryface/cbt-django-backend/blob/master/LICENSE.txt
