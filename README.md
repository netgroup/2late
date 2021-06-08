<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/netgroup/2late">
    <img src="doc/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    Proxy-reencryption module for offline devices
  </p>
</p>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/netgroup/2late)

Access control in offline, non tamper-proof, low-power devices presents very hard challenges. Among the others, how to properly handle with user revocation primes. 
This is the implementation of a new ElGamal inspired cryptosystem called BURBLE based on a lightweight active security data storage protecting a secret stored on a device. 
A proxy re-encryption service allows to continuously change encryption keys, so that only authorized users can have access to the secret. On their hand, authorized users need to contact a trusted authority to obtain the short-time decryption keys, thus centralising the access control the remote devices. The system offers a protection against attackers even if provided with old keys. 
Thanks to the key rotation, even they tamper the device, they will not get access to the secret as the re-encryption operation likely happened as they arrive too late.

Key features:
* Access control (based on time and data) for offline devices with key revocation
* Perfect forward secrecy also in case of device tampering
* Efficient key derivation for offline devices


### Built With

* [pyca/cryptography](https://cryptography.io/)



<!-- GETTING STARTED -->
## Getting Started

We provide the code for two entity: the Key Management System (KMS) and a device.

* KMS: is an authority which provides a key to the user to access to a given data at a given time. 
* Device: is an offline devices which encrypt a data repository and periodically re-encrypt with the proposed algorithm. User may decrypt a given data at a given time only if provided with the right key by the KMS.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
* Install python modules 
  ```sh
  pip install -r requirements.txt 
  ```


<!-- USAGE EXAMPLES -->
## Usage


1. Encrypt a repository of data, e.g. the "data" directory. Encrypted files will be stored in another directory, e.g., the "enc" directory.
   ```sh
   cd device
   python encrypt.py data enc
   ```
   Each file will be encrypted with a salt corresponding to the name of the directory containing it. For instance dir1/data1 will be encrypted with the salt "dir1"

2. Decrypt the file. Since no re-encryption has been performed yet, we can generate from the KMS, the key for time t=0 and salt "dir1" as:
   ```sh
   cd kms
   python gen_key.py 0 "dir1"
   ```
   This will give us the decryption key:
   ```sh
   Key: 5832594713651757220202868487364375832954501204190174057528304176309677882792148217209267373848653034879456307702649692718474965542306232324905256654225129183424444560603952533607639039676737637856089872368413189548046569821600471257083711089710879234888585914708984950812008591529352870399132902081960350562985495574571306719538213731667438234178838506510239152106146918152042410513304707726581787044411077415481262331936320153734193684531813173830114027756374187981781936187037555752776997085342721372788514647586185265287417865663015515183897805255657368015414489197689639148885311916892408204148826282393822842650
   ```
   We can thus apply such key to decrypt dir1/data1 in the "enc" folder.
   ```sh
   python decrypt.py enc/dir1/data1 5832594713651757220202868487364375832954501204190174057528304176309677882792148217209267373848653034879456307702649692718474965542306232324905256654225129183424444560603952533607639039676737637856089872368413189548046569821600471257083711089710879234888585914708984950812008591529352870399132902081960350562985495574571306719538213731667438234178838506510239152106146918152042410513304707726581787044411077415481262331936320153734193684531813173830114027756374187981781936187037555752776997085342721372788514647586185265287417865663015515183897805255657368015414489197689639148885311916892408204148826282393822842650
   ```
   This will return the file content in clear text form.
3. Run the re-encryption module as:
   ```sh
   python reencrypt.py enc
   ```
   This will re-encrypt all the files inside the enc directory, using as salt the subdirectory (e.g., "dir1").
   Re-encryptions happen periodically. If we stop it at time t=1 (after one re-encryption) we can decrypt the file provided that we have the right key.

4. Decrypt the file at a given time t. For instance after the first re-encryption (t=1) we can get the right key from the KMS as:
   ```sh 
   python get_key.py 1 dir1
    ```
   Obtain the key:
   ```sh 
   Key: 23522653000798673895740299869131224889429719918398478042519422099272584135547865428327416654720807038151490135079960300523853897992271263288280381124295444140229504962811825847015405118013534672092838259348244759963778367007878906184946969958179187937620434580878927675045588941689168505931231311868276502765106338120363495975475759551393814364627478626833418498009669483694523782179566742886283462326102805815406185428702675584968419951766759376075066032355636615883548065987879743984708807463840627842920009231628480276329237622540685603088179902775971479936143897867466305352653314484324208086967741847031575225339
   ```
   And then use the key to decrypt the file:
   ```sh
   python decrypt.py enc/dir1/data1 23522653000798673895740299869131224889429719918398478042519422099272584135547865428327416654720807038151490135079960300523853897992271263288280381124295444140229504962811825847015405118013534672092838259348244759963778367007878906184946969958179187937620434580878927675045588941689168505931231311868276502765106338120363495975475759551393814364627478626833418498009669483694523782179566742886283462326102805815406185428702675584968419951766759376075066032355636615883548065987879743984708807463840627842920009231628480276329237622540685603088179902775971479936143897867466305352653314484324208086967741847031575225339
   ```
   This will return the file content in a clear text form

   


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

* Lorenzo Bracciale - lorenzo.bracciale@uniroma2.it
* Pierpalo Loreti - pierpaolo.loreti@uniroma2.it
* Emanuele Raso - emanuele.raso@uniroma2.it
* Giuseppe Bianchi - giuseppe.bianchi@uniroma2.it

The work has been submitted to publication.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: doc/images/smart_lock_1.png
