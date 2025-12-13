import { useState, useRef } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import Icon from '@/components/ui/icon';
import { useToast } from '@/hooks/use-toast';

interface ProfileEditProps {
  initialData: {
    avatar: string;
    nickname: string;
    description: string;
  };
  onSave: (data: { avatar: string; nickname: string; description: string }) => void;
}

const ProfileEdit = ({ initialData, onSave }: ProfileEditProps) => {
  const [avatar, setAvatar] = useState(initialData.avatar);
  const [nickname, setNickname] = useState(initialData.nickname);
  const [description, setDescription] = useState(initialData.description);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast({
          title: 'Ошибка',
          description: 'Файл слишком большой. Максимум 5 МБ',
          variant: 'destructive'
        });
        return;
      }
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatar(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    if (!nickname.trim()) {
      toast({
        title: 'Ошибка',
        description: 'Укажите никнейм',
        variant: 'destructive'
      });
      return;
    }

    onSave({ avatar, nickname, description });
    toast({
      title: 'Сохранено!',
      description: 'Профиль успешно обновлен'
    });
  };

  return (
    <Card className="p-8 animate-scale-in">
      <div className="space-y-6 max-w-2xl mx-auto">
        <div className="flex flex-col items-center space-y-4">
          <Avatar className="w-32 h-32 border-4 border-primary/10">
            <AvatarImage src={avatar} alt={nickname} />
            <AvatarFallback className="bg-accent text-accent-foreground text-4xl">
              <Icon name="User" size={48} />
            </AvatarFallback>
          </Avatar>
          
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            className="hidden"
          />
          
          <Button
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
            className="gap-2"
          >
            <Icon name="Upload" size={16} />
            Загрузить аватарку
          </Button>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="nickname">Никнейм</Label>
            <Input
              id="nickname"
              placeholder="Введите никнейм"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              maxLength={50}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Описание</Label>
            <Textarea
              id="description"
              placeholder="Расскажите о себе..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={5}
              maxLength={500}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground text-right">
              {description.length}/500
            </p>
          </div>
        </div>

        <Button onClick={handleSave} className="w-full gap-2" size="lg">
          <Icon name="Save" size={18} />
          Сохранить профиль
        </Button>
      </div>
    </Card>
  );
};

export default ProfileEdit;
