Does the base image need refreshing?

Navigate to the parent directory (/backend).

Follow the steps below. It automatically uses your current poetry.lock for packages:

`docker build --file=base_image/Dockerfile -t algreg_base . `
`docker tag algreg_base harbor.cicd.s15m.nl/ictu-devops-pub/algreg_base`
`docker login harbor.cicd.s15m.nl`
`docker push harbor.cicd.s15m.nl/ictu-devops-pub/algreg_base`

or as a one-liner:

`docker build --file=base_image/Dockerfile -t algreg_base . && docker tag algreg_base harbor-gn2.cicd.s15m.nl/ictu-devops-pub/algreg_base && docker login harbor-gn2.cicd.s15m.nl && docker push harbor-gn2.cicd.s15m.nl/ictu-devops-pub/algreg_base`
