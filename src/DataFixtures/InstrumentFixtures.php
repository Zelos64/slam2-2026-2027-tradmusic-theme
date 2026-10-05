<?php
namespace App\DataFixtures;

use App\Entity\Instrument;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;

class InstrumentFixtures extends Fixture
{
    public function load(ObjectManager $manager): void
    {
        $instruments = [
            'Banjo' => 'banjo.svg',
            'Bodhran' => 'bodhran.svg',
            'Concertina' => 'concertina.svg',
            'Fiddle' => 'fiddle.svg',
            'Flute' => 'flute.svg',
            'Guitar' => 'guitar.svg',
            'Harp' => 'harp.svg',
            'Tin Whistle' => 'tin-whistle.svg',
            'Uilleann Pipes' => 'uilleann-pipes.svg',
        ];

        foreach ($instruments as $name => $icon) {
            $instrument = new Instrument();
            $instrument->setName($name);
            $instrument->setIcon($icon);
            $manager->persist($instrument);
        }

        $manager->flush();
    }
}