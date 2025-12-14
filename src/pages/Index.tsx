import { useState } from 'react';
import ProfileView from '@/components/ProfileView';
import ProfileEdit from '@/components/ProfileEdit';
import SupportChat from '@/components/SupportChat';
import Snowfall from '@/components/Snowfall';
import { Button } from '@/components/ui/button';
import Icon from '@/components/ui/icon';

const Index = () => {
  const [currentView, setCurrentView] = useState<'profile' | 'edit' | 'support'>('profile');
  const [profileData, setProfileData] = useState({
    avatar: '',
    nickname: 'Пользователь',
    description: 'Добро пожаловать в мой профиль'
  });

  const handleSaveProfile = (data: typeof profileData) => {
    setProfileData(data);
    setCurrentView('profile');
  };

  return (
    <div className="min-h-screen relative">
      <Snowfall />
      <nav className="border-b border-white/20 bg-white/10 backdrop-blur-md sticky top-0 z-40 shadow-lg">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-4xl">
          <h1 className="text-xl font-bold text-white drop-shadow-lg">✨ Профили</h1>
          <div className="flex gap-2">
            <Button
              variant={currentView === 'profile' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setCurrentView('profile')}
              className="gap-2"
            >
              <Icon name="User" size={16} />
              Профиль
            </Button>
            <Button
              variant={currentView === 'edit' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setCurrentView('edit')}
              className="gap-2"
            >
              <Icon name="Settings" size={16} />
              Редактировать
            </Button>
            <Button
              variant={currentView === 'support' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setCurrentView('support')}
              className="gap-2"
            >
              <Icon name="MessageCircle" size={16} />
              Поддержка
            </Button>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="animate-fade-in">
          {currentView === 'profile' && <ProfileView {...profileData} />}
          {currentView === 'edit' && (
            <ProfileEdit 
              initialData={profileData} 
              onSave={handleSaveProfile} 
            />
          )}
          {currentView === 'support' && <SupportChat />}
        </div>
      </main>
    </div>
  );
};

export default Index;