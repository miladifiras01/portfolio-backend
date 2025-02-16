from sqlmodel import Session
from app.database import engine
from app.models import *
from datetime import datetime

projects_data = [
    {
        "id": 1,
        "name": "Goodlead",
        "description": """<p>Goodle is a Software as a Service (SaaS) platform designed to bridge the gap between employees' professional skills and the needs of NGOs.</p>
  <p>By combining these two elements, Goodle facilitates volunteer work in a meaningful way, strengthening the social impact of businesses and helping NGOs achieve their goals more effectively.</p>
  <p>Developed with Dotnet and React JS.</p>
  <p>In the context of this year-end project carried out with two other colleagues, my main tasks included:</p>
  <p>Developing the search filter, designing the sign-up and login interfaces, and modifying the user interface (UI) to make the platform responsive, ensuring optimal use across all types of devices (desktops, tablets, mobiles).</p>
 """,
        "short_description": "A corporate social responsibility (CSR) platform aimed at engaging businesses in impactful initiatives.",
        "github_url": "https://github.com",
        "created_at": datetime.fromisoformat("2025-02-16T21:51:08.670701"),
        "technologies": [
            {"id": 18, "name": "Next.js"},
            {"id": 19, "name": "React"},
            {"id": 20, "name": "TypeScript"},
            {"id": 21, "name": "GitHub"},
            {"id": 22, "name": ".NET (C#)"},
        ],
        "images": [
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656651/portfolio/jyoqfsjriliyxprst44d.png",
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656657/portfolio/iz78hhcbpx50niswa9v0.png",
        ],
    },
    {
        "id": 2,
        "name": "Eventizer",
        "description": """<p>Eventizer is a platform dedicated to organizing large-scale events and conferences, developed using Laravel and Angular.</p>
  <p>My role involved updating certain features, such as email functionality and displaying participant data, as well as fixing existing bugs.</p>
  <p>Skills and Technologies Learned:</p>
  <p>Laravel, Angular, API Integration, HTML, CSS, Typescript, Gitlab.</p> """,
        "short_description": "An event management platform that facilitates mass emailing, certificate distribution, and improved client communication.",
        "github_url": "https://github.com",
        "created_at": datetime.fromisoformat("2025-02-16T21:51:08.674175"),
        "technologies": [
            {"id": 1, "name": "Angular JS"},
            {"id": 11, "name": "Laravel"},
            {"id": 12, "name": "GitLab"},
            {"id": 15, "name": "Rest API"},
        ],
        "images": [
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656658/portfolio/sx0zoemurjzwm2jhw8w2.png",
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656658/portfolio/xz3iu082xg8hzj1jpwh3.png",
        ],
    },
    {
        "id": 3,
        "name": "CRM - Big Brands Group",
        "description": """ <p>
    Big Brands Group (BBG) is an importer, exporter, distributor, and manufacturer specialized in consumer goods.
  </p>
  <p>
    I contributed to the development of a Customer Relationship Management (CRM) platform for BBG's sales team using Laravel and Angular. The platform includes several key features such as client management, order management, and catalog and product management.
  </p>
  <p>
    My role evolved throughout the project, initially participating in its initiation and later taking full responsibility for its completion, working independently with the Product Owner.
  </p>
  <p>
    Notable achievements include creating a 3D visualization feature for cargo shipments in containers using the Searates API, implementing a bulk client import feature from Excel files, and developing APIs for the mobile application, with a particular focus on access management and data security.
  </p> """,
        "short_description": "A customer relationship management (CRM) platform designed to streamline operations for Big Brands Group.",
        "github_url": "https://github.com",
        "created_at": datetime.fromisoformat("2025-02-16T21:51:08.677618"),
        "technologies": [
            {"id": 1, "name": "Angular JS"},
            {"id": 11, "name": "Laravel"},
            {"id": 12, "name": "GitLab"},
            {"id": 15, "name": "Rest API"},
            {"id": 16, "name": "ApexCharts"},
            {"id": 17, "name": "Maatwebsite Excel"},
        ],
        "images": [
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656655/portfolio/pwaaxb0ekornyvdtxdjj.png",
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656655/portfolio/ipt3u961p3jsk0f90u0y.png",
            "https://res.cloudinary.com/dmz6mdnsa/image/upload/v1739656655/portfolio/skwlrjvj7n79ml58y5ha.png",
        ],
    },
]


def seed_database():
    with Session(engine) as session:
        for project_data in projects_data:
            project = session.get(Project, project_data["id"])
            if not project:
                project = Project(
                    id=project_data["id"],
                    name=project_data["name"],
                    description=project_data["description"],
                    short_description=project_data["short_description"],
                    github_url=project_data["github_url"],
                    created_at=project_data["created_at"],
                )
                session.add(project)

            for tech_data in project_data["technologies"]:
                tech = session.get(Technology, tech_data["id"])
                if not tech:
                    tech = Technology(
                        id=tech_data["id"], name=tech_data["name"])
                    session.add(tech)
                link = session.get(ProjectTechnologyLink,
                                   (project.id, tech.id))
                if not link:
                    session.add(ProjectTechnologyLink(
                        project_id=project.id, technology_id=tech.id))

            for image_url in project_data["images"]:
                image = ProjectImages(
                    project_id=project.id, image_url=image_url)
                session.add(image)

        session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
