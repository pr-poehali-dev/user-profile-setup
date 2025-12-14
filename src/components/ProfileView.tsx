import { Card } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import Icon from '@/components/ui/icon';

interface ProfileViewProps {
  avatar: string;
  nickname: string;
  description: string;
}

const ProfileView = ({ avatar, nickname, description }: ProfileViewProps) => {
  return (
    <Card className="p-8 animate-scale-in">
      <div className="flex flex-col items-center text-center space-y-6">
        <Avatar className="w-32 h-32 border-4 border-primary/10">
          <AvatarImage src={avatar} alt={nickname} />
          <AvatarFallback className="bg-accent text-accent-foreground text-4xl">
            <Icon name="User" size={48} />
          </AvatarFallback>
        </Avatar>
        
        <div className="space-y-2 max-w-lg">
          <h2 className="text-3xl font-bold text-foreground">{nickname}</h2>
          <p className="text-muted-foreground text-lg leading-relaxed">
            {description}
          </p>
        </div>

        <Button 
          onClick={() => window.open('http://dubbingrp.tilda.ws/', '_blank')}
          className="mt-4"
        >
          <Icon name="ShoppingBag" className="mr-2" size={20} />
          Магазин
        </Button>
      </div>
    </Card>
  );
};

export default ProfileView;