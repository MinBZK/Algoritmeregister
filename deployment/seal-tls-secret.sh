# Make sure kubeseal is installed -> https://github.com/bitnami-labs/sealed-secrets/releases
CUR_DIR="$( cd "$( dirname "$0" )" && pwd )"

if [[ "$1" != "" ]] && [[ "$2" != "" ]] && [[ "$3" != "" ]] && [[ "$4" != "" ]]; then
    if [[ "$1" == "ictu-devops-prd" ]] ; then
        PUBLICKEY="overheid-prod.pem"
		PROJ="prd"
    else
        PUBLICKEY="overheid-test.pem"
		if [[ "$1" == "ictu-devops-acc" ]] ; then
			PROJ="acc"
		else
			PROJ="tst"
        fi
			
    fi
    NAMESPACE=$1
    CERT_NAME=$2
    TLS_KEY=$3
    TLS_CRT=$4
else
    echo "Requires namespace, inputfile, secretname as arguments, example: ./sealsecret.sh ictu-devops-acc /path/to/file/secrets.txt backend-secrets"
    echo "For creating file with different type add a 4th parameter with type, examples: kubernetes.io/dockercfg"
    echo "INPUTFILE for key=value pairs has to be have extension.txt, if the inputfile ext is not .txt it will take the filename as key and the file as input(keystores/full xmls)"
    exit;
fi

kubectl create secret tls ${CERT_NAME} --key ${TLS_KEY} --cert ${TLS_CRT} --dry-run -o yaml > ${CUR_DIR}/tmpsecret
echo "Encrypting secret using key ${PUBLICKEY} for namespace ${NAMESPACE} and project ${PROJ}"
echo ""

cat ${CUR_DIR}/tmpsecret
OUTPUTLOCATION=${CUR_DIR}/static/certificates/${PROJ}-${CERT_NAME}-encrypted.yaml
kubeseal --namespace ${NAMESPACE} --cert ${CUR_DIR}/sealedsecretpublickey/${PUBLICKEY} --format yaml < ${CUR_DIR}/tmpsecret > ${OUTPUTLOCATION}
rm ${CUR_DIR}/tmpsecret

echo ""
echo "Encrypted in ${OUTPUTLOCATION}"
