# Make sure kubeseal is installed -> https://github.com/bitnami-labs/sealed-secrets/releases
# RUN with [namespace] [secretfile(plaintext with key=value pairs)] [secretname] [type(optional, default Opaque. option-> docker]
# SEAL SECRETS WITH PROD PUBLIC KEY FOR PROD (./sealedsecretpublickey/overheid-prod.pem)
CUR_DIR="$( cd "$( dirname "$0" )" && pwd )"

if [[ "$1" != "" ]] && [[ "$2" != "" ]] && [[ "$3" != "" ]]; then
    if [[ "$1" == "ictu-devops-prd" ]]; then
        PUBLICKEY="overheid-prod.pem"
    else
        PUBLICKEY="overheid-test.pem"
    fi
    NAMESPACE=$1
    if [[ "$2" == *".txt" ]]; then
        FROMARG="--from-env-file"
    else
        FROMARG="--from-file"
    fi
    INPUTFILE=$2
    SECRETNAME=$3
    if [[ "$4" != "" ]]; then
        TYPE=$4
    else
        TYPE="Opaque"
    fi
else
    echo "Requires namespace, inputfile, secretname as arguments, example: ./sealsecret.sh ictu-devops-acc /path/to/file/secrets.txt backend-secrets"
    echo "For creating file with different type add a 4th parameter with type, examples: kubernetes.io/dockercfg"
    echo "INPUTFILE for key=value pairs has to be have extension.txt, if the inputfile ext is not .txt it will take the filename as key and the file as input(keystores/full xmls)"
    exit;
fi

kubectl create secret generic --type ${TYPE} ${SECRETNAME} --dry-run ${FROMARG}=${INPUTFILE} -o yaml > ${CUR_DIR}/tmpsecret
echo "Encrypting secret using key ${PUBLICKEY} for namespace ${NAMESPACE}:"
echo ""

cat ${CUR_DIR}/tmpsecret
OUTPUTLOCATION=${CUR_DIR}/${NAMESPACE}/${SECRETNAME}-encrypted.yaml
kubeseal --namespace ${NAMESPACE} --cert ${CUR_DIR}/sealedsecretpublickey/${PUBLICKEY} --format yaml < ${CUR_DIR}/tmpsecret > ${OUTPUTLOCATION}
rm ${CUR_DIR}/tmpsecret

echo ""
echo "Encrypted in ${OUTPUTLOCATION}"