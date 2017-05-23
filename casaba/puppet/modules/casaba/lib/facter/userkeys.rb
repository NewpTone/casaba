require 'facter'

Facter.add(:userkeys) do
  setcode do
    user_string = Facter::Core::Execution.exec("cat /etc/passwd |grep /home |grep /bin/bash |cut -d: -f1")
    user_lists = user_string.split(" ")
    userkeys = {}

    user_lists.each do |value|
      pubkey = Facter::Core::Execution.exec("[ -f /home/#{value}/.ssh/id_rsa.pub ] && cat /home/#{value}/.ssh/id_rsa.pub|awk {'print $2'}")
      if pubkey
        userkeys[value] = pubkey
      end
    end

    userkeys
  end
end
