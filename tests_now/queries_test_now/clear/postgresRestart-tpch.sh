host="cc11-small-node001 cc11-small-node002 cc11-small-node003 cc11-small-node004 cc11-small-node005 cc11-small-node006 cc11-small-node007 cc11-small-node008 cc11-small-node009 cc11-small-node010 cc11-small-node011  cc11-small-node012  ec2-52-13-100-8.us-west-2.compute.amazonaws.com ec2-54-214-138-55.us-west-2.compute.amazonaws.com ec2-54-184-84-108.us-west-2.compute.amazonaws.com ec2-52-13-113-187.us-west-2.compute.amazonaws.com ec2-52-13-14-225.us-west-2.compute.amazonaws.com ec2-54-189-175-159.us-west-2.compute.amazonaws.com ec2-54-212-13-77.us-west-2.compute.amazonaws.com ec2-54-189-164-130.us-west-2.compute.amazonaws.com ec2-54-189-165-174.us-west-2.compute.amazonaws.com ec2-52-12-93-140.us-west-2.compute.amazonaws.com ec2-54-188-30-47.us-west-2.compute.amazonaws.com ec2-54-185-25-50.us-west-2.compute.amazonaws.com"

CMD="sudo service postgresql restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$CMD'" ::: $host