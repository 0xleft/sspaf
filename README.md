# A horribly written single page application framework

(: SSPAF a superglued single page aooplication framework :)

Author: plusleft

Usage: `sspaf <operation> <path>`

Operations:
    render: render the project to the output folder
    serve: serve the project on port 8080
    publish: create a production ready version of the project
    create: initialize the blueprint for a new project

Path:
    path to the project

Examples:
    `sspaf serve .`

    `sspaf publish /home/plusleft/myproject`
    
    `sspaf create /home/plusleft/myproject`